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
FAMILIES = [  # (stats file stem, label in the figure)
    ("RQ1-dup", "RQ1a  S vs G-dup"),
    ("RQ1-proj", "RQ1b  S vs G-proj"),
    ("RQ2-bin", "RQ2  BEFORE vs IN-FOLD, T-bin"),
    ("RQ2-12", "RQ2  BEFORE vs IN-FOLD, T-12"),
    ("RQ3-Gdup", "RQ3  M5/M6 vs M1–M4, G-dup"),
    ("RQ3-S", "RQ3  M5/M6 vs M1–M4, S"),
    ("RQ2-D2", "Dalpiaz  BEFORE vs IN-FOLD"),
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


def table(label, caption, cols, header, rows, wide=False, size="\\small"):
    env = "table*" if wide else "table"
    return "\n".join([
        f"\\begin{{{env}}}[t]", "\\centering", f"\\caption{{{caption}}}", f"\\label{{{label}}}", size,
        "\\setlength{\\tabcolsep}{4pt}", f"\\begin{{tabular}}{{{cols}}}", "\\toprule", *header, "\\midrule",
        *rows, "\\bottomrule", "\\end{tabular}", f"\\end{{{env}}}", "",
    ])


NOTE = "Bold $\\Delta$: clear difference ($|\\Delta| \\geq 0.01$ and Holm-adjusted $p < 0.05$, corrected repeated k-fold $t$-test)."


def rq1():
    s = pd.read_csv(TABLES / "summary_RQ1.csv").set_index(["model", "protocol"])["mean"]
    dup = stats("RQ1-dup").assign(model=lambda x: x.comparison.str[:2]).set_index("model")
    proj = stats("RQ1-proj").assign(model=lambda x: x.comparison.str[:2]).set_index("model")
    rows = [f"M0 & {s['M0', 'S']:.3f} & {s['M0', 'G-dup']:.3f} & {s['M0', 'G-proj']:.3f} & -- & -- & -- & -- \\\\"]
    for m in MODELS:
        a, b = dup.loc[m], proj.loc[m]
        rows.append(f"{m} & {s[m, 'S']:.3f} & {s[m, 'G-dup']:.3f} & {s[m, 'G-proj']:.3f} & "
                    f"{mark(a)} & {p(a.p_holm)} & {mark(b)} & {p(b.p_holm)} \\\\")
    return table("tab:rq1",
                 "RQ1: macro-F1 under stratified CV (S), duplicate-grouped CV (G-dup) and project-grouped CV (G-proj) "
                 "on PROMISE\\_exp, T-bin, no oversampling (mean over 5 seeds $\\times$ 5 folds). "
                 f"$\\Delta$ = S $-$ grouped. {NOTE}",
                 "lccc rr rr",
                 ["& \\multicolumn{3}{c}{Macro-F1} & \\multicolumn{2}{c}{S $-$ G-dup} & \\multicolumn{2}{c}{S $-$ G-proj} \\\\",
                  "\\cmidrule(lr){2-4}\\cmidrule(lr){5-6}\\cmidrule(lr){7-8}",
                  "Model & S & G-dup & G-proj & $\\Delta$ & $p_{\\mathrm{Holm}}$ & $\\Delta$ & $p_{\\mathrm{Holm}}$ \\\\"],
                 rows, wide=True)


def parse_os(df):
    m = df.comparison.str.extract(r"^(M\d) (OS-[RS]):")
    return df.assign(model=m[0], os=m[1]).set_index(["model", "os"])


def rq2_rows(summary, task, st, dataset):
    s = summary[(summary.dataset == dataset) & (summary.task == task)].set_index(["model", "condition", "oversampler"])["mean"]
    out = []
    for (m, o), r in st.iterrows():
        out.append((m, o, s[m, "BEFORE", o], s[m, "IN-FOLD", o], r))
    return out


def rq2():
    summ = pd.read_csv(TABLES / "summary_RQ2.csv")
    rb = rq2_rows(summ, "T-bin", parse_os(stats("RQ2-bin")), PROMISE)
    r12 = {(m, o): rest for m, o, *rest in rq2_rows(summ, "T-12", parse_os(stats("RQ2-12")), PROMISE)}
    rows = []
    for m, o, bb, bi, sb in rb:
        tb, ti, s12 = r12[m, o]
        rows.append(f"{m} & {o} & {bb:.3f} & {bi:.3f} & {mark(sb)} & {p(sb.p_holm)} & "
                    f"{tb:.3f} & {ti:.3f} & {mark(s12)} & {p(s12.p_holm)} \\\\")
    return table("tab:rq2",
                 "RQ2: macro-F1 when oversampling is applied to the whole dataset before splitting (BEFORE) versus "
                 "inside each training fold only (IN-FOLD), PROMISE\\_exp, stratified CV. OS-R: random oversampling; "
                 f"OS-S: SMOTE. $\\Delta$ = BEFORE $-$ IN-FOLD. {NOTE}",
                 "ll cc rr cc rr",
                 ["& & \\multicolumn{4}{c}{T-bin (FR vs NFR)} & \\multicolumn{4}{c}{T-12 (12 classes)} \\\\",
                  "\\cmidrule(lr){3-6}\\cmidrule(lr){7-10}",
                  "Model & OS & BEFORE & IN-FOLD & $\\Delta$ & $p_{\\mathrm{Holm}}$ & BEFORE & IN-FOLD & $\\Delta$ & $p_{\\mathrm{Holm}}$ \\\\"],
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
    st = parse_os(stats("RQ2-D2"))
    rows = []
    for m, r in lodo.iterrows():
        a, b = st.loc[(m, "OS-R")], st.loc[(m, "OS-S")]
        rows.append(f"{m} & {r.mean_S:.3f} & {r.mean_LODO:.3f} & {d(r.delta_S_minus_LODO)} & "
                    f"{mark(a)} ({p(a.p_holm)}) & {mark(b)} ({p(b.p_holm)}) \\\\")
    return table("tab:dalpiaz",
                 "Replication on the Dalpiaz et al.\\ dataset ($n=327$, 4 projects), T-bin, macro-F1. "
                 "S vs leave-one-dataset-out (LODO) is descriptive only (25 vs 4 folds cannot be paired). "
                 "Right: $\\Delta$ = BEFORE $-$ IN-FOLD with Holm-adjusted $p$ in brackets. " + NOTE,
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
                 "lccr", ["Model & Full & No-both & $\\Delta$ \\\\"], rows)


def none_vs_infold():
    df = pd.read_csv(TABLES / "descriptive_none_vs_infold_RQ2.csv")
    rows = []
    for (m, o), g in df.groupby(["model", "oversampler"]):
        g = g.set_index("task")
        rows.append(f"{m} & {o} & {g.loc['T-bin', 'mean_none']:.3f} & {g.loc['T-bin', 'mean_in_fold']:.3f} & "
                    f"{d(-g.loc['T-bin', 'delta_none_minus_in_fold'])} & {g.loc['T-12', 'mean_none']:.3f} & "
                    f"{g.loc['T-12', 'mean_in_fold']:.3f} & {d(-g.loc['T-12', 'delta_none_minus_in_fold'])} \\\\")
    return table("tab:none_infold",
                 "Effect of correct (IN-FOLD) oversampling against no oversampling (NONE), PROMISE\\_exp, stratified CV, "
                 "macro-F1. $\\Delta$ = IN-FOLD $-$ NONE. Descriptive only.",
                 "ll ccr ccr",
                 ["& & \\multicolumn{3}{c}{T-bin} & \\multicolumn{3}{c}{T-12} \\\\",
                  "\\cmidrule(lr){3-5}\\cmidrule(lr){6-8}",
                  "Model & OS & NONE & IN-FOLD & $\\Delta$ & NONE & IN-FOLD & $\\Delta$ \\\\"],
                 rows)


def kendall():
    df = pd.read_csv(TABLES / "kendall_tau.csv")
    name = {PROMISE: "PROMISE\\_exp", DALPIAZ: "Dalpiaz"}
    rows = [f"{name[r.dataset]} & {r.protocol_x} vs {r.protocol_y} & {r.models.replace(' ', ', ')} & {r.kendall_tau:.3f} \\\\"
            for r in df.itertuples()]
    return table("tab:kendall",
                 "Agreement of model rankings (mean macro-F1, T-bin, no oversampling) between evaluation protocols "
                 "(Kendall's $\\tau$).",
                 "llp{2.6cm}r", ["Dataset & Protocols & Models & $\\tau$ \\\\"], rows)


def summary_figure():
    """One dot per comparison, grouped by family: filled = clear difference, hollow = not. Grayscale-safe."""
    plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.linewidth": 0.6})
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ink, muted = "#1f2937", "#9ca3af"
    for i, (name, label) in enumerate(FAMILIES):
        y = len(FAMILIES) - 1 - i
        st = stats(name)
        clear = st.decision != "no clear difference"
        jitter = [((k % 5) - 2) * 0.07 for k in range(len(st))]
        ys = [y + j for j in jitter]
        ax.scatter(st.mean_delta[~clear], [v for v, c in zip(ys, clear) if not c], s=16,
                   facecolors="white", edgecolors=ink, linewidths=0.8, zorder=3)
        ax.scatter(st.mean_delta[clear], [v for v, c in zip(ys, clear) if c], s=16, color=ink, zorder=3)
        ax.text(-0.03, y, label, ha="right", va="center", fontsize=7, transform=ax.get_yaxis_transform())
        ax.text(1.02, y, f"{clear.sum()}/{len(st)}", ha="left", va="center", fontsize=7,
                transform=ax.get_yaxis_transform())
    ax.axvline(0, color=muted, linewidth=0.6, zorder=1)
    ax.axvspan(-0.01, 0.01, color="#e5e7eb", zorder=0, linewidth=0)
    ax.set_yticks([])
    ax.set_ylim(-0.6, len(FAMILIES) - 0.4)
    ax.set_xlabel("$\\Delta$ macro-F1 (A $-$ B)")
    ax.grid(axis="x", color="#e5e7eb", linewidth=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.scatter([], [], s=16, color=ink, label="clear difference")
    ax.scatter([], [], s=16, facecolors="white", edgecolors=ink, linewidths=0.8, label="no clear difference")
    ax.legend(loc="lower right", fontsize=6.5, frameon=False, handletextpad=0.2)
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
