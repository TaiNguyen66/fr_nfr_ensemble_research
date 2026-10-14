import numpy as np
import pandas as pd
import pytest

from src.experiment import run_config
from src.models import MODEL_IDS, HardVoting, Stacking, make_model
from src.run_experiments import plan, protocol_locked
from src.stats import compare_family, corrected_ttest, decide, holm

FR = ["the user shall {} the {}", "the system shall allow users to {} a {}", "admins shall {} each {}"]
NFR = ["the {} shall respond within {} seconds", "the {} must be available {} percent of the time",
       "the {} shall be secure and {} encrypted"]
VERBS = ["create", "delete", "view", "edit", "export", "print", "search", "approve"]
NOUNS = ["report", "account", "order", "file", "invoice", "schedule", "ticket", "record"]


def synthetic(n_per_class=40, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_per_class):
        rows.append((rng.choice(FR).format(rng.choice(VERBS), rng.choice(NOUNS)), "FR", "F"))
        t = rng.choice(NFR).format(rng.choice(NOUNS), int(rng.integers(1, 99)))
        rows.append((t, "NFR", ["PE", "A", "SE"][i % 3]))
    df = pd.DataFrame(rows, columns=["text", "label_bin", "label_12"])
    df.insert(0, "requirement_id", [f"X{i:03d}" for i in range(len(df))])
    df["project_id"] = [f"p{i % 8}" for i in range(len(df))]
    df["duplicate_group"] = np.arange(len(df))
    return df


@pytest.mark.parametrize("model_id", MODEL_IDS)
def test_every_model_learns_synthetic_data(model_id):
    df = synthetic()
    folds, preds = run_config(df, "T-bin", model_id, "S", seed=42, n_splits=3)
    assert len(folds) == 3 and len(preds) == len(df)
    floor = 0.3 if model_id == "M0" else 0.9
    assert folds.macro_f1.mean() >= floor


def test_hard_voting_tie_goes_to_m2():
    hv = HardVoting()
    hv.bases_ = [type("B", (), {"predict": lambda self, X, v=v: np.array([v] * len(X))})() for v in ("A", "B", "C")]
    hv.classes_ = np.array(["A", "B", "C"])
    assert list(hv.predict(["x", "y"])) == ["B", "B"]


def test_stacking_inner_splits_stay_in_outer_train():
    df = synthetic()
    from src.splits import make_folds
    tr, te = make_folds(df, "G-proj", 42, 4)[0]
    st = Stacking(seed=42).fit(df.text.to_numpy(object)[tr], df.label_bin.to_numpy()[tr],
                               groups=df.project_id.to_numpy()[tr])
    test_ids = set(te)
    for itr, iva in st.inner_splits_:
        outer_rows = set(tr[itr]) | set(tr[iva])
        assert not outer_rows & test_ids
        g = df.project_id.to_numpy()[tr]
        assert not set(g[itr]) & set(g[iva])  # same splitter type as the outer protocol


@pytest.mark.parametrize("oversampler", ["OS-R", "OS-S"])
@pytest.mark.parametrize("condition", ["IN-FOLD", "BEFORE"])
def test_oversampling_conditions(condition, oversampler):
    df = synthetic().iloc[:70]  # imbalanced: 35 FR, 35 NFR → drop some NFR
    df = pd.concat([df[df.label_bin == "FR"], df[df.label_bin == "NFR"].iloc[:15]], ignore_index=True)
    folds, preds = run_config(df, "T-bin", "M1", "S", condition, oversampler, seed=42, n_splits=3)
    n_eval = folds.n_test.sum()
    if condition == "IN-FOLD":
        assert n_eval == len(df) and (preds.row_id != "SYN").all()
    else:
        assert n_eval == 2 * (df.label_bin == "FR").sum()  # test folds come from the oversampled set


def test_in_fold_keeps_test_rows_original():
    df = synthetic()
    _, preds = run_config(df, "T-12", "M2", "S", "IN-FOLD", "OS-S", seed=42, n_splits=3)
    assert sorted(preds.row_id) == sorted(df.requirement_id)


def test_before_rejects_grouped_protocol():
    with pytest.raises(ValueError):
        run_config(synthetic(), "T-bin", "M1", "G-dup", "BEFORE", "OS-R")


def test_corrected_ttest_and_holm():
    rng = np.random.default_rng(1)
    a = 0.80 + rng.normal(0, 0.01, 25)
    r = corrected_ttest(a + 0.05, a, 0.25)
    assert r["mean_delta"] == pytest.approx(0.05) and r["p"] < 0.001 and r["ci_low"] > 0
    same = corrected_ttest(a, a, 0.25)
    assert same["p"] == 1.0
    d = rng.normal(0.01, 0.02, 25)
    r = corrected_ttest(a + d, a, 0.25)
    naive_half = 2.064 * d.std(ddof=1) / 5
    assert (r["ci_high"] - r["ci_low"]) / 2 > naive_half  # correction widens the CI
    assert list(holm([0.01, 0.04, 0.03])) == pytest.approx([0.03, 0.06, 0.06])


def test_decision_rule():
    assert decide(0.02, 0.01) == "A > B"
    assert decide(-0.02, 0.01) == "A < B"
    assert decide(0.005, 0.0001) == "no clear difference"
    assert decide(0.05, 0.2) == "no clear difference"
    rows = compare_family({"x": ([0.9] * 25, [0.8] * 25)}, 0.25)
    assert rows[0]["decision"] == "A > B"


def test_plan_sizes_match_protocol():
    assert len(list(plan("RQ1"))) == 21
    assert len(list(plan("RQ2"))) == 50
    assert len(list(plan("D2"))) == 5 * 7


def test_lock_guard(tmp_path):
    p = tmp_path / "protocol.md"
    p.write_text("| Status | **DRAFT** until both members sign |\n", encoding="utf-8")
    assert not protocol_locked(p)
    p.write_text("| Status | **LOCKED** (2026-10-17) |\n", encoding="utf-8")
    assert protocol_locked(p)
