"""One configuration = task × model × protocol × oversampling × seed → per-fold scores + predictions."""
import numpy as np
import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold

from src.models import make_model, make_sampler, make_tfidf
from src.splits import make_folds

CONDITIONS = ("NONE", "IN-FOLD", "BEFORE")
LABEL_COL = {"T-bin": "label_bin", "T-12": "label_12"}
GROUP_COL = {"G-dup": "duplicate_group", "G-proj": "project_id", "LODO": "project_id"}


def _metrics(y_true, y_pred):
    return {"macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
            "accuracy": accuracy_score(y_true, y_pred),
            "macro_precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
            "macro_recall": recall_score(y_true, y_pred, average="macro", zero_division=0)}


def _before(df, label, oversampler, seed, n_splits):
    """BEFORE (§7.2): oversample the whole dataset, then split it with protocol S (leaky by design)."""
    y = df[label].to_numpy()
    if oversampler == "OS-R":
        idx, _ = RandomOverSampler(random_state=seed).fit_resample(np.arange(len(df)).reshape(-1, 1), y)
        data = df.iloc[idx.ravel()].reset_index(drop=True)
        X, yo, vectorize = data["text"].to_numpy(dtype=object), data[label].to_numpy(), True
    else:
        Xv = make_tfidf().fit_transform(df["text"])  # fitted on all rows, as in the reviewed studies
        X, yo = make_sampler("OS-S", seed, y).fit_resample(Xv, y)
        n_syn = X.shape[0] - len(df)
        data = pd.concat([df, pd.DataFrame({"requirement_id": ["SYN"] * n_syn, "label_bin": None,
                                            "project_id": None, "duplicate_group": -1})], ignore_index=True)
        data[label] = yo
        vectorize = False
    folds = list(StratifiedKFold(n_splits, shuffle=True, random_state=seed).split(np.zeros(len(yo)), yo))
    return data, X, yo, folds, vectorize


def run_config(df, task, model_id, protocol, condition="NONE", oversampler=None, seed=42, n_splits=5):
    label = LABEL_COL[task]
    if condition == "BEFORE":
        if protocol != "S":
            raise ValueError("BEFORE is only defined under protocol S")
        data, X, y, folds, vectorize = _before(df, label, oversampler, seed, n_splits)
    else:
        data, X, y = df.reset_index(drop=True), df["text"].to_numpy(dtype=object), df[label].to_numpy()
        folds, vectorize = make_folds(data, protocol, seed, n_splits, label=label), True
    in_fold = oversampler if condition == "IN-FOLD" else None
    groups = data[GROUP_COL[protocol]].to_numpy() if protocol in GROUP_COL else None

    fold_rows, preds = [], []
    for k, (tr, te) in enumerate(folds):
        model = make_model(model_id, seed, in_fold, vectorize)
        model.fit(X[tr], y[tr], groups=None if groups is None else groups[tr])
        y_pred = model.predict(X[te])
        s = model.scores(X[te])
        fold_rows.append({"task": task, "model": model_id, "protocol": protocol, "condition": condition,
                          "oversampler": oversampler or "", "seed": seed, "fold": k,
                          "n_train": len(tr), "n_test": len(te), **_metrics(y[te], y_pred)})
        preds.append(pd.DataFrame({
            "row_id": data["requirement_id"].iloc[te].to_numpy(),
            "project_id": data["project_id"].iloc[te].to_numpy(),
            "duplicate_group": data["duplicate_group"].iloc[te].to_numpy() if "duplicate_group" in data else -1,
            "true_label": y[te], "predicted_label": y_pred,
            "score": s[:, 0] if s.shape[1] == 1 else s.max(axis=1),
            "fold": k, "seed": seed, "task": task, "model": model_id, "protocol": protocol,
            "oversampling": condition if not oversampler else f"{condition}/{oversampler}"}))
    return pd.DataFrame(fold_rows), pd.concat(preds, ignore_index=True)
