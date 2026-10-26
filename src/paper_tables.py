"""Build LaTeX tables and the summary figure for the paper from results/tables/*.csv.

No number is typed by hand: every value comes from the analysis outputs.
Run: python -m src.paper_tables  -> paper/tables/*.tex, paper/figures/*.pdf|png
"""
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "results" / "tables"
OUT = ROOT / "paper" / "tables"
FIG = ROOT / "paper" / "figures"
MODELS = ["M1", "M2", "M3", "M4", "M5", "M6"]
PROMISE, DALPIAZ, NOBOTH = "requirements.csv", "dalpiaz_requirements.csv", "dalpiaz_requirements_noboth.csv"
FAMILIES = [  # (file stem, label in the figure, tested?) — A-009: only RQ3 is tested
    ("RQ1-dup", "RQ1a  S vs G-dup", False),
    ("RQ1-proj", "RQ1b  S vs G-proj", False),
    ("RQ2-bin", "RQ2  BEFORE vs IN-FOLD, T-bin", False),
    ("RQ2-12", "RQ2  BEFORE vs IN-FOLD, T-12", False),
    ("RQ2-D2", "Dalpiaz  BEFORE vs IN-FOLD", False),
    ("RQ3-Gdup", "RQ3  M5/M6 vs M1–M4, G-dup", True),
    ("RQ3-S", "RQ3  M5/M6 vs M1–M4, S", True),
]


def fmt(mean, sd):
    return f"{mean:.3f} $\\pm$ {sd:.3f}"


def d(x):
    return f"{x:+.3f}"


def p(x):
    return "$<$0.001" if x < 0.001 else f"{x:.3f}"


def mark(row):
    """Bold the delta when the §10 rule (|Δ| ≥ 0.01 and Holm p < 0.05) calls it a clear difference."""
    s = d(row.mean_delta)
    return s if row.decision == "no clear difference" else f"\\textbf{{{s}}}"


def stats(name):
    return pd.read_csv(TABLES / f"stats_{name}.csv")


def desc(name):
    """Descriptive comparison family (A-009): mean_a, sd_a, mean_b, sd_b, mean_delta per comparison."""
    return pd.read_csv(TABLES / f"descriptive_{name}.csv")


def msd(mean, sd):
    return f"{mean:.3f} $\\pm$ {sd:.3f}"


DESC = ("Descriptive only: the protocols use different test folds, so no paired test is applied "
        "(mean $\\pm$ SD over 5 seeds $\\times$ 5 folds).")


def table(label, caption, cols, header, rows, wide=False, size="\\small", pos="t"):
    env = "table*" if wide else "table"
    return "\n".join([
        f"\\begin{{{env}}}[{pos}]", "\\centering", f"\\caption{{{caption}}}", f"\\label{{{label}}}", size,
        "\\setlength{\\tabcolsep}{4pt}", f"\\begin{{tabular}}{{{cols}}}", "\\toprule", *header, "\\midrule",
        *rows, "\\bottomrule", "\\end{tabular}", f"\\end{{{env}}}", "",
    ])


NOTE = "Bold $\\Delta$: clear difference ($|\\Delta| \\geq 0.01$ and Holm-adjusted $p < 0.05$, corrected repeated k-fold $t$-test)."


def rq1():
    s = pd.read_csv(TABLES / "summary_RQ1.csv").set_index(["model", "protocol"])
    dup = desc("RQ1-dup").assign(model=lambda x: x.comparison.str[:2]).set_index("model")
    proj = desc("RQ1-proj").assign(model=lambda x: x.comparison.str[:2]).set_index("model")
    cell = lambda m, pr: msd(s.loc[(m, pr), "mean"], s.loc[(m, pr), "sd"])
    rows = [f"M0 & {cell('M0', 'S')} & {cell('M0', 'G-dup')} & {cell('M0', 'G-proj')} & -- & -- \\\\"]
    for m in MODELS:
        rows.append(f"{m} & {cell(m, 'S')} & {cell(m, 'G-dup')} & {cell(m, 'G-proj')} & "
                    f"{d(dup.loc[m, 'mean_delta'])} & {d(proj.loc[m, 'mean_delta'])} \\\\")
    return table("tab:rq1",
                 "RQ1: macro-F1 under stratified CV (S), duplicate-grouped CV (G-dup) and project-grouped CV (G-proj) "
                 "on PROMISE\\_exp, T-bin, no oversampling. $\\Delta$ = S $-$ grouped (difference of means). " + DESC,
                 "lccc rr",
                 ["& \\multicolumn{3}{c}{Macro-F1} & \\multicolumn{2}{c}{$\\Delta$} \\\\",
                  "\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}",
                  "Model & S & G-dup & G-proj & S $-$ G-dup & S $-$ G-proj \\\\"],
                 rows, wide=True)


def rq2():
    s = pd.read_csv(TABLES / "summary_RQ2.csv")
    s = s[s.dataset == PROMISE].set_index(["task", "model", "condition", "oversampler"])
    cell = lambda task, m, c, o: msd(s.loc[(task, m, c, o), "mean"], s.loc[(task, m, c, o), "sd"])
    rows = []
    for m in ("M1", "M2", "M3", "M4", "M5"):
        for o in ("OS-R", "OS-S"):
            parts = []
            for task in ("T-bin", "T-12"):
                delta = s.loc[(task, m, "BEFORE", o), "mean"] - s.loc[(task, m, "IN-FOLD", o), "mean"]
                parts.append(f"{cell(task, m, 'BEFORE', o)} & {cell(task, m, 'IN-FOLD', o)} & {d(delta)}")
            rows.append(f"{m} & {o} & {parts[0]} & {parts[1]} \\\\")
    return table("tab:rq2",
                 "RQ2: macro-F1 when oversampling is applied to the whole dataset before splitting (BEFORE) versus "
                 "inside each training fold only (IN-FOLD), PROMISE\\_exp, stratified CV. OS-R: random oversampling; "
                 "OS-S: SMOTE. $\\Delta$ = BEFORE $-$ IN-FOLD (difference of means). Descriptive only: BEFORE test folds "
                 "are drawn from the oversampled set, so they are not the IN-FOLD test rows and no paired test is applied "
                 "(mean $\\pm$ SD over 5 seeds $\\times$ 5 folds).",
                 "ll ccr ccr",
                 ["& & \\multicolumn{3}{c}{T-bin (FR vs NFR)} & \\multicolumn{3}{c}{T-12 (12 classes)} \\\\",
                  "\\cmidrule(lr){3-5}\\cmidrule(lr){6-8}",
                  "Model & OS & BEFORE & IN-FOLD & $\\Delta$ & BEFORE & IN-FOLD & $\\Delta$ \\\\"],
                 rows, wide=True)


def rq3():
    g, s = stats("RQ3-Gdup"), stats("RQ3-S")
    rows = []
    for (_, a), (_, b) in zip(g.iterrows(), s.iterrows()):
        name = a.comparison.split(" (")[0]
        rows.append(f"{name} & {mark(a)} & [{a.ci_low:+.3f}, {a.ci_high:+.3f}] & {p(a.p_holm)} & "
                    f"{mark(b)} & {p(b.p_holm)} \\\\")
    return table("tab:rq3",
                 "RQ3: ensembles (M5 hard voting, M6 stacking) versus single classifiers M1--M4, PROMISE\\_exp, T-bin, "
                 "macro-F1. $\\Delta$ = ensemble $-$ single; 95\\% CI from the corrected $t$-test (unadjusted). "
                 f"G-dup is the primary protocol; S is reported for comparison. {NOTE}",
                 "l rcr rr",
                 ["& \\multicolumn{3}{c}{G-dup (primary)} & \\multicolumn{2}{c}{S} \\\\",
                  "\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}",
                  "Comparison & $\\Delta$ & 95\\% CI & $p_{\\mathrm{Holm}}$ & $\\Delta$ & $p_{\\mathrm{Holm}}$ \\\\"],
                 rows)


def dalpiaz():
    lodo = pd.read_csv(TABLES / "descriptive_RQ1-D2_S_vs_LODO.csv").set_index("model")
    st = desc("RQ2-D2")
    m_os = st.comparison.str.extract(r"^(M\d) (OS-[RS]):")
    st = st.assign(model=m_os[0], os=m_os[1]).set_index(["model", "os"])
    rows = []
    for m, r in lodo.iterrows():
        rows.append(f"{m} & {r.mean_S:.3f} & {r.mean_LODO:.3f} & {d(r.delta_S_minus_LODO)} & "
                    f"{d(st.loc[(m, 'OS-R'), 'mean_delta'])} & {d(st.loc[(m, 'OS-S'), 'mean_delta'])} \\\\")
    return table("tab:dalpiaz",
                 "Replication on the Dalpiaz et al.\\ dataset ($n=327$, 4 projects), T-bin, macro-F1 (means). "
                 "Left: stratified CV (S) vs leave-one-dataset-out (LODO). Right: $\\Delta$ = BEFORE $-$ IN-FOLD. "
                 "All comparisons are descriptive (different test folds; S has 25 folds, LODO 4).",
                 "l cc r rr",
                 ["& \\multicolumn{3}{c}{Evaluation protocol} & \\multicolumn{2}{c}{BEFORE $-$ IN-FOLD} \\\\",
                  "\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}",
                  "Model & S & LODO & $\\Delta$ & OS-R & OS-S \\\\"],
                 rows)


def noboth_d2():
    """Appendix: Dalpiaz full vs. no-both sensitivity, T-bin, protocol S, no oversampling (descriptive)."""
    s = pd.read_csv(TABLES / "summary_D2.csv")
    s = s[(s.task == "T-bin") & (s.protocol == "S") & (s.condition == "NONE")].set_index(["dataset", "model"])
    folds = pd.read_csv(TABLES / "fold_scores_D2.csv")
    n = {k: int((g.n_train + g.n_test).iloc[0]) for k, g in folds[folds.protocol == "S"].groupby("dataset")}
    rows = []
    for m in MODELS:
        if (NOBOTH, m) not in s.index:
            continue
        a, b = s.loc[(DALPIAZ, m)], s.loc[(NOBOTH, m)]
        rows.append(f"{m} & {fmt(a['mean'], a['sd'])} & {fmt(b['mean'], b['sd'])} & {d(b['mean'] - a['mean'])} \\\\")
    return table("tab:noboth",
                 "Sensitivity of the Dalpiaz replication to removing requirements labelled both F and Q "
                 f"(T-bin, S, no oversampling; macro-F1 mean $\\pm$ SD over 25 folds; full $n={n[DALPIAZ]}$, "
                 f"no-both $n={n[NOBOTH]}$). Descriptive only.",
                 "lccr", ["Model & Full & No-both & $\\Delta$ \\\\"], rows, pos="!htb")


def none_vs_infold():
    """Appendix: IN-FOLD vs NONE (descriptive). Two stacked panels (T-bin, T-12) so the table fits one column;
    NONE does not depend on the oversampler, so it is shown once per model."""
    df = pd.read_csv(TABLES / "descriptive_none_vs_infold_RQ2.csv")
    rows = []
    for i, (task, title) in enumerate([("T-bin", "T-bin (FR vs NFR)"), ("T-12", "T-12 (12 classes)")]):
        if i:
            rows.append("\\midrule")
        rows.append(f"\\multicolumn{{6}}{{l}}{{\\textit{{{title}}}}} \\\\")
        g = df[df.task == task].set_index(["model", "oversampler"])
        for m in sorted(g.index.get_level_values("model").unique()):
            r, s = g.loc[(m, "OS-R")], g.loc[(m, "OS-S")]
            rows.append(f"{m} & {r['mean_none']:.3f} & {r['mean_in_fold']:.3f} & {d(-r['delta_none_minus_in_fold'])} & "
                        f"{s['mean_in_fold']:.3f} & {d(-s['delta_none_minus_in_fold'])} \\\\")
    return table("tab:none_infold",
                 "Effect of correct (IN-FOLD) oversampling against no oversampling (NONE), PROMISE\\_exp, stratified CV, "
                 "macro-F1. OS-R: random oversampling; OS-S: SMOTE. $\\Delta$ = IN-FOLD $-$ NONE. Descriptive only.",
                 "l c cr cr",
                 ["& & \\multicolumn{2}{c}{IN-FOLD, OS-R} & \\multicolumn{2}{c}{IN-FOLD, OS-S} \\\\",
                  "\\cmidrule(lr){3-4}\\cmidrule(lr){5-6}",
                  "Model & NONE & F1 & $\\Delta$ & F1 & $\\Delta$ \\\\"],
                 rows, pos="!htb")


def kendall():
    df = pd.read_csv(TABLES / "kendall_tau.csv")
    name = {PROMISE: "PROMISE\\_exp", DALPIAZ: "Dalpiaz"}
    rows = [f"{name[r.dataset]} & {r.protocol_x} vs {r.protocol_y} & {r.models.replace(' ', ', ')} & {r.kendall_tau:.3f} \\\\"
            for r in df.itertuples()]
    return table("tab:kendall",
                 "Agreement of model rankings (mean macro-F1, T-bin, no oversampling) between evaluation protocols "
                 "(Kendall's $\\tau$).",
                 "llp{2.6cm}r", ["Dataset & Protocols & Models & $\\tau$ \\\\"], rows, pos="!htb")


def summary_figure():
    """One dot per comparison, grouped by family. RQ3 (tested): filled = clear difference, hollow = not.
    Cross-protocol/condition families (A-009): grey crosses, descriptive only. Grayscale-safe."""
    plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.linewidth": 0.6})
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ink, muted, grey = "#1f2937", "#9ca3af", "#6b7280"
    for i, (name, label, tested) in enumerate(FAMILIES):
        y = len(FAMILIES) - 1 - i
        st = stats(name) if tested else desc(name)
        jitter = [((k % 5) - 2) * 0.07 for k in range(len(st))]
        ys = [y + j for j in jitter]
        if tested:
            clear = st.decision != "no clear difference"
            ax.scatter(st.mean_delta[~clear], [v for v, c in zip(ys, clear) if not c], s=16,
                       facecolors="white", edgecolors=ink, linewidths=0.8, zorder=3)
            ax.scatter(st.mean_delta[clear], [v for v, c in zip(ys, clear) if c], s=16, color=ink, zorder=3)
            right = f"{clear.sum()}/{len(st)}"
        else:
            ax.scatter(st.mean_delta, ys, s=18, marker="x", color=grey, linewidths=0.8, zorder=3)
            right = "desc."
        ax.text(-0.03, y, label, ha="right", va="center", fontsize=7, transform=ax.get_yaxis_transform())
        ax.text(1.02, y, right, ha="left", va="center", fontsize=7, transform=ax.get_yaxis_transform())
    ax.axhline(1.5, color="#e5e7eb", linewidth=0.6, zorder=0)
    ax.axvline(0, color=muted, linewidth=0.6, zorder=1)
    ax.axvspan(-0.01, 0.01, color="#e5e7eb", zorder=0, linewidth=0)
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(FAMILIES) - 0.4)
    ax.set_xlabel("$\\Delta$ macro-F1 (A $-$ B)")
    ax.grid(axis="x", color="#e5e7eb", linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.scatter([], [], s=18, marker="x", color=grey, linewidths=0.8, label="descriptive (no test)")
    ax.scatter([], [], s=16, color=ink, label="RQ3: clear difference")
    ax.scatter([], [], s=16, facecolors="white", edgecolors=ink, linewidths=0.8, label="RQ3: no clear difference")
    ax.legend(loc="lower right", fontsize=6, frameon=False, handletextpad=0.2)
    FIG.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"summary_deltas.{ext}", bbox_inches="tight", dpi=300)
    plt.close(fig)


def rq2_t12_figure():
    """Slide figure: macro-F1 of NONE / IN-FOLD / BEFORE per model on T-12 (OS-R), one row per model."""
    s = pd.read_csv(TABLES / "summary_RQ2.csv")
    s = s[(s.task == "T-12") & ((s.oversampler == "OS-R") | (s.condition == "NONE"))]
    plt.rcParams.update({"font.size": 11, "font.family": "sans-serif"})
    fig, ax = plt.subplots(figsize=(7, 3.6))
    models = ["M1", "M2", "M3", "M4", "M5"]
    styles = {"NONE": dict(marker="o", facecolors="white", edgecolors="#6b7280"),
              "IN-FOLD": dict(marker="o", color="#1f2937"),
              "BEFORE": dict(marker="D", color="#b91c1c")}
    for y, m in enumerate(reversed(models)):
        v = s[s.model == m].set_index("condition")["mean"]
        ax.plot([v["IN-FOLD"], v["BEFORE"]], [y, y], color="#d1d5db", linewidth=2, zorder=1)
        for c, st in styles.items():
            ax.scatter(v[c], y, s=70, zorder=3, label=c if y == 0 else None, **st)
    ax.set_yticks(range(len(models)), list(reversed(models)))
    ax.set_xlim(0.2, 1.02)
    ax.set_xlabel("macro-F1 (12 classes, random oversampling)")
    ax.grid(axis="x", color="#e5e7eb", linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="lower left", frameon=False, ncol=3, bbox_to_anchor=(0, 1.0))
    fig.savefig(FIG / "slide_rq2_t12.png", bbox_inches="tight", dpi=300)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("rq1", rq1), ("rq2", rq2), ("rq3", rq3), ("dalpiaz", dalpiaz), ("noboth_d2", noboth_d2),
                     ("none_vs_infold", none_vs_infold), ("kendall", kendall)]:
        (OUT / f"{name}.tex").write_text(fn(), encoding="utf-8")
    summary_figure()
    rq2_t12_figure()
    print(f"Wrote tables to {OUT} and summary_deltas.pdf/png to {FIG}")


if __name__ == "__main__":
    main()
