"""Build duplicate groups and write the processed tables (protocol §4.1–4.2).

    python -m src.audit_dataset            # requires the `final` column of the near-duplicate review
    python -m src.audit_dataset --draft    # falls back to `proposal` where `final` is empty (not for model runs)
"""
import argparse
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data import ROOT, canonical, load_dalpiaz, load_promise_exp
from src.splits import groups_crossing_folds

REVIEW = ROOT / "data/processed/near_duplicate_review.csv"
NEAR_DUP_THRESHOLD = 0.90


def _find(parent, i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i


def near_duplicate_candidates(df, threshold=NEAR_DUP_THRESHOLD):
    """Pairs of first-row indices of distinct canonical groups with char 3–5-gram cosine >= threshold."""
    can = df["text"].map(canonical)
    firsts = can.drop_duplicates()
    X = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5)).fit_transform(firsts.values)
    S = cosine_similarity(X)
    idx = firsts.index.to_numpy()
    i, j = np.where(np.triu(S, k=1) >= threshold)
    return [(int(idx[a]), int(idx[b]), float(S[a, b])) for a, b in zip(i, j)]


def duplicate_groups(df, same_pairs=()):
    """Exact canonical groups merged with reviewed SAME pairs (union-find). Labels are not used."""
    can = df["text"].map(canonical).to_numpy()
    first = {}
    parent = list(range(len(df)))
    for i, c in enumerate(can):
        parent[i] = first.setdefault(c, i)
    for a, b in same_pairs:
        ra, rb = _find(parent, a), _find(parent, b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)
    roots = [_find(parent, i) for i in range(len(df))]
    order = {r: k for k, r in enumerate(dict.fromkeys(roots))}
    return np.array([order[r] for r in roots])


def reviewed_same_pairs(path=REVIEW, draft=False):
    rv = pd.read_csv(path, encoding="utf-8-sig")
    final = rv["final"].fillna("").astype(str).str.strip().str.upper()
    if (final == "").any():
        if not draft:
            raise SystemExit(f"{(final == '').sum()} near-duplicate pairs have no `final` decision; "
                             "fill them in or use --draft (not for model runs).")
        final = final.where(final != "", rv["proposal"].str.upper())
    return [(int(a), int(b)) for a, b, f in zip(rv.row_a, rv.row_b, final) if f == "SAME"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", action="store_true")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    df = load_promise_exp()
    cand = near_duplicate_candidates(df)
    same = reviewed_same_pairs(draft=args.draft)
    df["duplicate_group"] = duplicate_groups(df, same)
    sizes = df.groupby("duplicate_group").size()
    multi = sizes[sizes > 1].index
    conflicts = df[df.duplicate_group.isin(multi)].groupby("duplicate_group").label_bin.nunique().gt(1).sum()
    print(f"PROMISE_exp: {len(df)} rows, {df.project_id.nunique()} projects, "
          f"{df.label_bin.value_counts().to_dict()}, {df.label_12.nunique()} classes")
    print(f"  near-duplicate candidates >= {NEAR_DUP_THRESHOLD}: {len(cand)}; SAME merged: {len(same)}")
    print(f"  duplicate groups with > 1 row: {len(multi)} ({int(sizes[multi].sum())} rows); label conflicts (bin): {conflicts}")
    print(f"  groups crossing folds under S (5 seeds): {groups_crossing_folds(df)}")
    df.to_csv(ROOT / "data/processed/requirements.csv", index=False, encoding="utf-8")

    for drop_both, name in ((False, "dalpiaz_requirements.csv"), (True, "dalpiaz_requirements_noboth.csv")):
        d = load_dalpiaz(drop_both=drop_both)
        d["duplicate_group"] = duplicate_groups(d)
        print(f"Dalpiaz2019{' (no both)' if drop_both else ''}: {len(d)} rows, "
              f"{d.label_bin.value_counts().to_dict()}, duplicate rows: {len(d) - d.duplicate_group.nunique()}")
        d.to_csv(ROOT / "data/processed" / name, index=False, encoding="utf-8")
    if args.draft:
        print("DRAFT: groups use the `proposal` column where `final` is empty; rerun without --draft before model runs.")


if __name__ == "__main__":
    main()
