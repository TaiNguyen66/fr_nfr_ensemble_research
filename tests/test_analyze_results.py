import numpy as np
import pandas as pd
import pytest

from src import analyze_results as ar
from src.run_experiments import plan
from src.splits import SEEDS


def fake_scores(plan_name, shift=None):
    """Synthetic fold_scores with the runner's columns; shift(config) adds a known effect."""
    rng = np.random.default_rng(0)
    rows = []
    for f, task, m, p, c, o in plan(plan_name):
        seeds = [0] if p == "LODO" else SEEDS
        for seed in seeds:
            for k in range(4 if p == "LODO" else 5):
                base = 0.80 + (shift(m, p, c) if shift else 0.0)
                rows.append({"dataset": f, "task": task, "model": m, "protocol": p, "condition": c,
                             "oversampler": o or "", "seed": seed, "fold": k, "n_train": 775, "n_test": 194,
                             "macro_f1": base + rng.normal(0, 0.005), "accuracy": 0.8,
                             "macro_precision": 0.8, "macro_recall": 0.8})
    return pd.DataFrame(rows)


def test_family_sizes_match_protocol():
    sizes = {n: len(c) for p in ("RQ1", "RQ2", "D2") for n, c in ar.families(p, fake_scores(p)).items()}
    assert sizes == {"RQ1-dup": 6, "RQ1-proj": 6, "RQ3-Gdup": 8, "RQ3-S": 8,
                     "RQ2-bin": 10, "RQ2-12": 10, "RQ2-D2": 10}


def test_known_effect_detected_and_null_not():
    df = fake_scores("RQ1", shift=lambda m, p, c: 0.05 if p == "S" else 0.0)
    st = ar.run_family(df, ar.families("RQ1", df)["RQ1-proj"])
    assert (st.decision == "A > B").all() and st.mean_delta.between(0.045, 0.055).all()
    assert st.n.eq(25).all() and st.test_train_ratio.iloc[0] == pytest.approx(194 / 775)
    st3 = ar.run_family(df, ar.families("RQ1", df)["RQ3-S"])
    assert (st3.decision == "no clear difference").all()


def test_before_vs_infold_direction():
    df = fake_scores("RQ2", shift=lambda m, p, c: 0.03 if c == "BEFORE" else 0.0)
    st = ar.run_family(df, ar.families("RQ2", df)["RQ2-12"])
    assert (st.decision == "A > B").all()


def test_pairing_requires_same_seed_fold():
    df = fake_scores("RQ1")
    df = df[~((df.model == "M1") & (df.protocol == "G-dup") & (df.fold == 4))]
    with pytest.raises(ValueError):
        ar.paired(df, ar._cfg(model="M1"), ar._cfg(model="M1", protocol="G-dup"))


def test_descriptive_and_tau():
    d2 = fake_scores("D2", shift=lambda m, p, c: {"M1": .01, "M2": .02, "M3": .03, "M4": .04, "M5": .05}[m])
    desc = ar.descriptive("D2", d2)
    assert len(desc["RQ1-D2_S_vs_LODO"]) == 5 and desc["RQ1-D2_S_vs_LODO"].n_LODO.eq(4).all()
    assert len(desc["none_vs_infold_D2"]) == 10
    assert ar.taus("D2", d2)[0]["kendall_tau"] == pytest.approx(1.0)


def test_main_writes_outputs(tmp_path):
    tables, figures = tmp_path / "tables", tmp_path / "figures"
    tables.mkdir()
    for p in ("RQ1", "RQ2", "D2"):
        fake_scores(p).to_csv(tables / f"fold_scores_{p}.csv", index=False)
    ar.main([], tables=tables, figures=figures)
    for name in ("RQ1-dup", "RQ1-proj", "RQ3-Gdup", "RQ3-S", "RQ2-bin", "RQ2-12", "RQ2-D2"):
        assert (tables / f"stats_{name}.csv").exists() and (figures / f"delta_{name}.png").exists()
    assert len(pd.read_csv(tables / "kendall_tau.csv")) == 3
