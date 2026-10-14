"""Models M0–M6 (protocol §6–7) with optional in-fold oversampling (§7.2).

Every model takes raw requirement texts. P0 preprocessing and TF-IDF are fitted on the
training part only. With vectorize=False the models take TF-IDF rows instead (BEFORE + SMOTE).
"""
import numpy as np
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold
from sklearn.naive_bayes import ComplementNB
from sklearn.svm import LinearSVC

from src.data import preprocess_p0

MODEL_IDS = ("M0", "M1", "M2", "M3", "M4", "M5", "M6")
BASE_IDS = ("M1", "M2", "M3")


def make_tfidf():
    return TfidfVectorizer(preprocessor=preprocess_p0, ngram_range=(1, 2), min_df=2, sublinear_tf=True,
                           lowercase=False, token_pattern=r"(?u)\b\w\w+\b")


def make_sampler(oversampler, seed, y):
    if oversampler == "OS-R":
        return RandomOverSampler(random_state=seed)
    if oversampler == "OS-S":
        n_min = int(np.unique(y, return_counts=True)[1].min())
        return SMOTE(random_state=seed, k_neighbors=max(1, min(5, n_min - 1)))
    raise ValueError(f"Unknown oversampler {oversampler!r}")


def _classifier(model_id, seed):
    return {
        "M0": lambda: DummyClassifier(strategy="most_frequent"),
        "M1": lambda: LogisticRegression(C=1.0, max_iter=2000),
        "M2": lambda: LinearSVC(C=1.0),
        "M3": lambda: RandomForestClassifier(n_estimators=300, random_state=seed, n_jobs=-1),
        "M4": lambda: ComplementNB(alpha=1.0),
    }[model_id]()


class SingleModel(BaseEstimator, ClassifierMixin):
    """[TF-IDF] → [oversampler, train part only] → classifier."""

    def __init__(self, model_id, seed=42, oversampler=None, vectorize=True):
        self.model_id, self.seed, self.oversampler, self.vectorize = model_id, seed, oversampler, vectorize

    def fit(self, X, y, groups=None):
        steps = [("tfidf", make_tfidf())] if self.vectorize else []
        if self.oversampler:
            steps.append(("os", make_sampler(self.oversampler, self.seed, y)))
        steps.append(("clf", _classifier(self.model_id, self.seed)))
        self.pipe_ = Pipeline(steps).fit(X, y)
        self.classes_ = self.pipe_.classes_
        return self

    def predict(self, X):
        return self.pipe_.predict(X)

    def scores(self, X):
        """Continuous scores, one column per class (binary: one column for classes_[1])."""
        clf = self.pipe_[-1]
        if hasattr(clf, "decision_function") and not hasattr(clf, "predict_proba"):
            s = self.pipe_.decision_function(X)
        else:
            s = self.pipe_.predict_proba(X)
            if s.shape[1] == 2:
                s = s[:, 1]
        return s.reshape(len(s), -1)


class HardVoting(BaseEstimator, ClassifierMixin):
    """M5: majority vote of M1, M2, M3; ties (only possible with > 2 classes) go to M2."""

    def __init__(self, seed=42, oversampler=None, vectorize=True):
        self.seed, self.oversampler, self.vectorize = seed, oversampler, vectorize

    def fit(self, X, y, groups=None):
        self.bases_ = [SingleModel(m, self.seed, self.oversampler, self.vectorize).fit(X, y) for m in BASE_IDS]
        self.classes_ = self.bases_[0].classes_
        return self

    def predict(self, X):
        P = np.column_stack([b.predict(X) for b in self.bases_])
        out = P[:, 1].copy()  # M2 = tie-break
        for i, row in enumerate(P):
            vals, counts = np.unique(row, return_counts=True)
            if counts.max() >= 2:
                out[i] = vals[counts.argmax()]
        return out

    def scores(self, X):
        """Share of base models voting for each class (binary: for classes_[1])."""
        P = np.column_stack([b.predict(X) for b in self.bases_])
        s = np.column_stack([(P == c).mean(axis=1) for c in self.classes_])
        return s[:, 1:] if len(self.classes_) == 2 else s


class Stacking(BaseEstimator, ClassifierMixin):
    """M6 (§7.1): inner 5-fold OOF scores of M1–M3 on the outer-training rows → LogisticRegression.

    The inner splitter has the same type as the outer protocol: StratifiedKFold when groups is None,
    otherwise StratifiedGroupKFold on the same groups. The outer test rows are never seen in fit().
    """

    def __init__(self, seed=42, oversampler=None, vectorize=True, n_inner=5):
        self.seed, self.oversampler, self.vectorize, self.n_inner = seed, oversampler, vectorize, n_inner

    def _inner_splits(self, X, y, groups):
        dummy = np.zeros(len(y))
        if groups is None:
            return list(StratifiedKFold(self.n_inner, shuffle=True, random_state=self.seed).split(dummy, y))
        return list(StratifiedGroupKFold(self.n_inner, shuffle=True, random_state=self.seed).split(dummy, y, groups))

    def _base(self, m):
        return SingleModel(m, self.seed, self.oversampler, self.vectorize)

    def fit(self, X, y, groups=None):
        X, y = _rows(X), np.asarray(y)
        self.inner_splits_ = self._inner_splits(X, y, groups)
        oof = None
        for tr, va in self.inner_splits_:
            cols = [self._base(m).fit(_take(X, tr), y[tr]).scores(_take(X, va)) for m in BASE_IDS]
            block = np.hstack(cols)
            if oof is None:
                oof = np.zeros((len(y), block.shape[1]))
            oof[va] = block
        self.meta_ = LogisticRegression(C=1.0, max_iter=2000).fit(oof, y)
        self.bases_ = [self._base(m).fit(X, y) for m in BASE_IDS]
        self.classes_ = self.meta_.classes_
        return self

    def _meta_X(self, X):
        return np.hstack([b.scores(X) for b in self.bases_])

    def predict(self, X):
        return self.meta_.predict(self._meta_X(X))

    def scores(self, X):
        s = self.meta_.predict_proba(self._meta_X(X))
        return s[:, 1:] if s.shape[1] == 2 else s


def _rows(X):
    """Row-indexable input: sparse TF-IDF matrices stay as they are, texts become an object array."""
    return X if hasattr(X, "tocsr") else np.asarray(X, dtype=object)


def _take(X, idx):
    return X[idx]


def make_model(model_id, seed=42, oversampler=None, vectorize=True):
    if model_id == "M5":
        return HardVoting(seed, oversampler, vectorize)
    if model_id == "M6":
        return Stacking(seed, oversampler, vectorize)
    return SingleModel(model_id, seed, oversampler, vectorize)
