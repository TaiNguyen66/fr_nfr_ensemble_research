"""Outer CV splits (protocol §8, A-007).

S       StratifiedKFold(5, shuffle, seed)
G-dup   StratifiedGroupKFold(5, shuffle, seed), groups = duplicate_group
G-proj  StratifiedGroupKFold(5, shuffle, seed), groups = project_id
LODO    LeaveOneGroupOut on project_id (Dalpiaz2019 only; deterministic, seed ignored)
"""
import numpy as np
from sklearn.model_selection import LeaveOneGroupOut, StratifiedGroupKFold, StratifiedKFold

SEEDS = (42, 123, 2026, 3407, 9917)
PROTOCOLS = ("S", "G-dup", "G-proj", "LODO")
_GROUP_COL = {"G-dup": "duplicate_group", "G-proj": "project_id", "LODO": "project_id"}


def make_folds(df, protocol, seed, n_splits=5, label="label_bin"):
    """List of (train_idx, test_idx) positional arrays; invariants are asserted."""
    y = df[label].to_numpy()
    X = np.zeros(len(df))
    if protocol == "S":
        folds = list(StratifiedKFold(n_splits, shuffle=True, random_state=seed).split(X, y))
    elif protocol in ("G-dup", "G-proj"):
        g = df[_GROUP_COL[protocol]].to_numpy()
        folds = list(StratifiedGroupKFold(n_splits, shuffle=True, random_state=seed).split(X, y, g))
    elif protocol == "LODO":
        folds = list(LeaveOneGroupOut().split(X, y, df["project_id"].to_numpy()))
    else:
        raise ValueError(f"Unknown protocol {protocol!r}")
    check_folds(df, folds, protocol)
    return folds


def check_folds(df, folds, protocol):
    seen = np.concatenate([te for _, te in folds])
    assert len(seen) == len(df) and len(np.unique(seen)) == len(df), "test folds must partition the rows"
    for tr, te in folds:
        assert not set(tr) & set(te), "train and test overlap"
        if protocol in _GROUP_COL:
            g = df[_GROUP_COL[protocol]].to_numpy()
            assert not set(g[tr]) & set(g[te]), f"{protocol}: a group is in both train and test"


def fold_stats(df, folds, label="label_bin", minority="FR"):
    out = []
    for k, (_, te) in enumerate(folds):
        y = df[label].to_numpy()[te]
        share = (y == minority).mean()
        out.append({"fold": k, "n_test": len(te), "row_share": len(te) / len(df),
                    "n_projects": df["project_id"].iloc[te].nunique(),
                    "min_class_share": min(share, 1 - share)})
    return out


def gproj_feasible(df, n_splits=5, seeds=SEEDS, min_projects=2, min_rows=0.10, min_class=0.20):
    """§8 rule: every test fold of every seed has >= 2 projects, >= 10% rows, >= 20% of each class."""
    for seed in seeds:
        for s in fold_stats(df, make_folds(df, "G-proj", seed, n_splits)):
            if s["n_projects"] < min_projects or s["row_share"] < min_rows or s["min_class_share"] < min_class:
                return False
    return True


def groups_crossing_folds(df, seeds=SEEDS, n_splits=5):
    """Per seed: number of multi-row duplicate groups split across folds under S (§4.1)."""
    g = df["duplicate_group"].to_numpy()
    sizes = np.bincount(g)
    multi = np.flatnonzero(sizes > 1)
    out = []
    for seed in seeds:
        fold = np.empty(len(df), int)
        for k, (_, te) in enumerate(make_folds(df, "S", seed, n_splits)):
            fold[te] = k
        out.append(sum(len(set(fold[g == m])) > 1 for m in multi))
    return out
