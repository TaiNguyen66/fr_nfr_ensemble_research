"""Statistical analysis of fold scores (protocol §10, A-007). Reads results/tables/fold_scores_<plan>.csv.

    python -m src.analyze_results          # every plan whose fold_scores file exists

Writes results/tables/stats_<family>.csv (tested families, RQ3 only), descriptive_<name>.csv, summary_<plan>.csv,
kendall_tau.csv and results/figures/delta_<family>.png. Δ is always A − B as named in the 'comparison' column.

A-009 (2026-10-25): comparisons between different protocols (S vs G-dup / G-proj) or oversampling conditions
(BEFORE vs IN-FOLD) are reported descriptively only, because their test folds are different rows and cannot be
paired on (seed, fold). The corrected paired t-test is kept for RQ3, where models share the same splits.
"""
import argparse
import sys

import pandas as pd

from src.data import ROOT
from src.stats import compare_family, kendall_tau

TABLES = ROOT / "results/tables"
FIGURES = ROOT / "results/figures"
PROMISE, DALPIAZ, NOBOTH = "requirements.csv", "dalpiaz_requirements.csv", "dalpiaz_requirements_noboth.csv"
KEYS = ["dataset", "task", "model", "protocol", "condition", "oversampler"]


def load(plan, tables=TABLES):
    path = tables / f"fold_scores_{plan}.csv"
    if not path.exists():
        return None
    return pd.read_csv(path, keep_default_na=False)


def select(df, metric="macro_f1", **where):
    """Fold scores of one configuration, indexed by (seed, fold), with n_test / n_train per fold."""
    sel = df
    for k, v in where.items():
        sel = sel[sel[k] == v]
    if sel.empty:
        raise KeyError(f"No fold scores for {where}")
    sel = sel.set_index(["seed", "fold"]).sort_index()
    if sel.index.duplicated().any():
        raise ValueError(f"Several configurations match {where}")
    return sel[metric], sel["n_test"] / sel["n_train"]


def paired(df, a, b, metric="macro_f1"):
    """Scores of A and B matched on (seed, fold) (§10: same folds, same seeds) and the n_test/n_train ratio."""
    for key in ("dataset", "task", "protocol", "condition", "oversampler"):
        if a.get(key) != b.get(key):
            raise ValueError(f"A-009: no paired test across different {key} ({a.get(key)} vs {b.get(key)}): "
                             "test folds are not the same rows")
    sa, ra = select(df, metric, **a)
    sb, rb = select(df, metric, **b)
    if not sa.index.equals(sb.index):
        raise ValueError(f"(seed, fold) pairs differ between {a} and {b}")
    return sa.to_numpy(), sb.to_numpy(), float(pd.concat([ra, rb]).mean())


def run_family(df, comparisons, metric="macro_f1"):
    """comparisons: {name: (filters_a, filters_b)}. Holm across the family; ratio pooled over its folds."""
    pairs, ratios = {}, []
    for name, (a, b) in comparisons.items():
        sa, sb, r = paired(df, a, b, metric)
        pairs[name], ratios = (sa, sb), ratios + [r]
    ratio = sum(ratios) / len(ratios)
    out = pd.DataFrame(compare_family(pairs, ratio))
    out.insert(1, "test_train_ratio", ratio)
    return out


def _cfg(dataset=PROMISE, task="T-bin", model="M1", protocol="S", condition="NONE", oversampler=""):
    return dict(dataset=dataset, task=task, model=model, protocol=protocol, condition=condition,
                oversampler=oversampler)


def families(plan, df):
    """Tested families (§10): only RQ3, where models are compared on the same splits (A-009)."""
    fam = {}
    if plan == "RQ1":
        singles, ens = ("M1", "M2", "M3", "M4"), ("M5", "M6")
        for p, name in (("G-dup", "RQ3-Gdup"), ("S", "RQ3-S")):
            fam[name] = {f"{e} vs {m} ({p})": (_cfg(model=e, protocol=p), _cfg(model=m, protocol=p))
                         for e in ens for m in singles}
    return fam


def cross_families(plan, df):
    """Descriptive families (A-009): different protocols or oversampling conditions, so no paired test."""
    fam = {}
    if plan == "RQ1":
        for g, name in (("G-dup", "RQ1-dup"), ("G-proj", "RQ1-proj")):
            fam[name] = {f"{m}: S vs {g}": (_cfg(model=m), _cfg(model=m, protocol=g))
                         for m in ("M1", "M2", "M3", "M4", "M5", "M6")}
    elif plan in ("RQ2", "D2"):
        tasks = ("T-bin", "T-12") if plan == "RQ2" else ("T-bin",)
        dataset = PROMISE if plan == "RQ2" else DALPIAZ
        for task in tasks:
            name = {"RQ2": {"T-bin": "RQ2-bin", "T-12": "RQ2-12"}, "D2": {"T-bin": "RQ2-D2"}}[plan][task]
            fam[name] = {f"{m} {o}: BEFORE vs IN-FOLD": (
                _cfg(dataset, task, m, condition="BEFORE", oversampler=o),
                _cfg(dataset, task, m, condition="IN-FOLD", oversampler=o))
                for m in ("M1", "M2", "M3", "M4", "M5") for o in ("OS-R", "OS-S")}
    return fam


def describe_family(df, comparisons, metric="macro_f1"):
    """Mean and SD of A and B over their own folds and Δ = mean(A) − mean(B); no test, no pairing (A-009)."""
    rows = []
    for name, (a, b) in comparisons.items():
        sa, _ = select(df, metric, **a)
        sb, _ = select(df, metric, **b)
        rows.append({"comparison": name, "mean_a": sa.mean(), "sd_a": sa.std(ddof=1), "n_a": len(sa),
                     "mean_b": sb.mean(), "sd_b": sb.std(ddof=1), "n_b": len(sb), "mean_delta": sa.mean() - sb.mean()})
    return pd.DataFrame(rows)


def summary(df, metric="macro_f1"):
    g = df.groupby(KEYS, sort=False)[metric]
    return g.agg(mean="mean", sd="std", n_folds="count").reset_index()


def descriptive(plan, df):
    """Comparisons §10 reports without a test: NONE vs IN-FOLD (RQ2, D2) and S vs LODO (A-007, unpaired)."""
    out = {}
    s = summary(df).set_index(KEYS)["mean"]
    if plan in ("RQ2", "D2"):
        rows = []
        for (ds, task, m, p, c, o), v in s.items():
            if c == "IN-FOLD":
                rows.append({"dataset": ds, "task": task, "model": m, "oversampler": o, "mean_in_fold": v,
                             "mean_none": s[(ds, task, m, p, "NONE", "")],
                             "delta_none_minus_in_fold": s[(ds, task, m, p, "NONE", "")] - v})
        out[f"none_vs_infold_{plan}"] = pd.DataFrame(rows)
    if plan == "D2":
        sm = summary(df).set_index(KEYS)
        rows = []
        for m in ("M1", "M2", "M3", "M4", "M5"):
            a, b = sm.loc[(DALPIAZ, "T-bin", m, "S", "NONE", "")], sm.loc[(DALPIAZ, "T-bin", m, "LODO", "NONE", "")]
            rows.append({"model": m, "mean_S": a["mean"], "sd_S": a["sd"], "n_S": a["n_folds"],
                         "mean_LODO": b["mean"], "sd_LODO": b["sd"], "n_LODO": b["n_folds"],
                         "delta_S_minus_LODO": a["mean"] - b["mean"]})
        out["RQ1-D2_S_vs_LODO"] = pd.DataFrame(rows)
    return out


def taus(plan, df):
    s = summary(df).set_index(KEYS)["mean"]
    if plan == "RQ1":
        models, ds, others = ("M1", "M2", "M3", "M4", "M5", "M6"), PROMISE, ("G-dup", "G-proj")
    elif plan == "D2":
        models, ds, others = ("M1", "M2", "M3", "M4", "M5"), DALPIAZ, ("LODO",)
    else:
        return []
    base = {m: s[(ds, "T-bin", m, "S", "NONE", "")] for m in models}
    return [{"dataset": ds, "protocol_x": "S", "protocol_y": g, "models": " ".join(models),
             "kendall_tau": kendall_tau(base, {m: s[(ds, "T-bin", m, g, "NONE", "")] for m in models})}
            for g in others]


def plot_family(name, stats, path):
    """Forest plot: mean Δ with unadjusted 95% CI; filled marker = clear difference after Holm."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, grid = "#1f2937", "#6b7280", "#e5e7eb"
    n = len(stats)
    fig, ax = plt.subplots(figsize=(6.4, 0.38 * n + 1.1))
    y = list(range(n))[::-1]
    ax.axvline(0, color=muted, lw=1)
    for x in (-0.01, 0.01):
        ax.axvline(x, color=grid, lw=1, ls="--")
    ax.hlines(y, stats["ci_low"], stats["ci_high"], color=ink, lw=2)
    clear = stats["decision"] != "no clear difference"
    ax.scatter(stats["mean_delta"][clear], [v for v, c in zip(y, clear) if c], s=64, color=ink, zorder=3,
               label="clear difference (|Δ| ≥ 0.01, Holm p < 0.05)")
    ax.scatter(stats["mean_delta"][~clear], [v for v, c in zip(y, clear) if not c], s=64, facecolor="white",
               edgecolor=ink, lw=2, zorder=3, label="no clear difference")
    ax.set_yticks(y, stats["comparison"], fontsize=9, color=ink)
    ax.set_xlabel("Δ macro-F1 (A − B), unadjusted 95% CI", color=ink)
    ax.set_title(name, loc="left", color=ink, fontsize=11)
    ax.tick_params(colors=muted)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12 - 0.6 / n), ncol=2, frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main(argv=None, tables=TABLES, figures=FIGURES):
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-figures", action="store_true")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    figures.mkdir(parents=True, exist_ok=True)
    tau_rows, done = [], []
    for plan in ("RQ1", "RQ2", "D2"):
        df = load(plan, tables)
        if df is None:
            continue
        done.append(plan)
        summary(df).to_csv(tables / f"summary_{plan}.csv", index=False)
        for name, comps in families(plan, df).items():
            st = run_family(df, comps)
            st.to_csv(tables / f"stats_{name}.csv", index=False)
            if not args.no_figures:
                plot_family(name, st, figures / f"delta_{name}.png")
            print(f"{name}: {(st.decision != 'no clear difference').sum()}/{len(st)} clear differences")
        for name, comps in cross_families(plan, df).items():
            ds = describe_family(df, comps)
            ds.to_csv(tables / f"descriptive_{name}.csv", index=False)
            print(f"{name}: descriptive only (A-009), Δ {ds.mean_delta.min():+.3f} to {ds.mean_delta.max():+.3f}")
        for name, t in descriptive(plan, df).items():
            t.to_csv(tables / f"descriptive_{name}.csv", index=False)
        tau_rows += taus(plan, df)
    if tau_rows:
        pd.DataFrame(tau_rows).to_csv(tables / "kendall_tau.csv", index=False)
    if not done:
        raise SystemExit("No results/tables/fold_scores_<plan>.csv found. Run src.run_experiments first.")
    print(f"Analysed {', '.join(done)} → results/tables, results/figures")


if __name__ == "__main__":
    main()
