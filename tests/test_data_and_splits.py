import numpy as np
import pandas as pd
import pytest

from src.audit_dataset import duplicate_groups
from src.data import DALPIAZ_DIR, PROMISE_PATH, canonical, load_dalpiaz, load_promise_exp, preprocess_p0
from src.splits import SEEDS, gproj_feasible, make_folds

needs_promise = pytest.mark.skipif(not PROMISE_PATH.exists(), reason="raw PROMISE_exp not present")
needs_dalpiaz = pytest.mark.skipif(not DALPIAZ_DIR.exists(), reason="raw Dalpiaz2019 not present")


def toy():
    texts = ["The system shall log in.", "the system shall log in", "Fast response.", "fast response!",
             "Shall export PDF.", "Must be secure.", "Shall print.", "Must be usable.",
             "Shall delete users.", "Must load in 2s.", "Shall search.", "Must be portable."]
    return pd.DataFrame({"text": texts,
                         "label_bin": ["FR", "FR", "NFR", "NFR"] + ["FR", "NFR"] * 4,
                         "project_id": ["a", "b", "a", "c", "b", "c", "d", "d", "e", "e", "f", "f"]})


def test_canonical_and_p0():
    assert canonical("  The  System shall LOG in.;  ") == "the system shall log in"
    assert preprocess_p0("It CAN'T and won't  fail, isn't it") == "it cannot and will not fail, is not it"


def test_duplicate_groups_exact_and_merged():
    df = toy()
    g = duplicate_groups(df)
    assert g[0] == g[1] and g[2] == g[3] and len(set(g)) == 10
    g2 = duplicate_groups(df, same_pairs=[(4, 6)])
    assert g2[4] == g2[6] and len(set(g2)) == 9


@pytest.mark.parametrize("protocol", ["S", "G-dup", "G-proj"])
def test_grouped_folds_never_share_groups(protocol):
    df = toy()
    df["duplicate_group"] = duplicate_groups(df)
    for seed in SEEDS:
        folds = make_folds(df, protocol, seed, n_splits=2)
        assert len(folds) == 2  # invariants are asserted inside make_folds


def test_lodo_one_project_per_test_fold():
    df = toy()
    for _, te in make_folds(df, "LODO", 0):
        assert df.project_id.iloc[te].nunique() == 1


def test_folds_reproducible():
    df = toy()
    a = [te.tolist() for _, te in make_folds(df, "S", 42, n_splits=2)]
    b = [te.tolist() for _, te in make_folds(df, "S", 42, n_splits=2)]
    assert a == b


@needs_promise
def test_promise_exp_matches_audit():
    df = load_promise_exp()
    assert len(df) == 969 and df.project_id.nunique() == 47 and df.label_12.nunique() == 12
    assert (df.label_bin == "FR").sum() == 444
    df["duplicate_group"] = duplicate_groups(df)
    assert len(df) - df.duplicate_group.nunique() == 3  # 3 exact groups of 2 rows
    assert gproj_feasible(df)
    for protocol in ("S", "G-dup", "G-proj"):
        make_folds(df, protocol, 42)


@needs_dalpiaz
def test_dalpiaz_mapping_and_lodo():
    df = load_dalpiaz()
    assert len(df) == 327 and (df.label_bin == "FR").sum() == 187
    assert sorted(df.project_id.unique()) == ["dronology", "leeds", "reqview", "wasp"]
    assert len(load_dalpiaz(drop_both=True)) == 327 - 81
    assert len(make_folds(df, "LODO", 0)) == 4
