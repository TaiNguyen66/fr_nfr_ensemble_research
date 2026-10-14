"""Decision rules (protocol §10): corrected repeated k-fold t-test, Holm, Kendall's tau."""
import numpy as np
from scipy import stats

MIN_DELTA = 0.01
ALPHA = 0.05


def corrected_ttest(a, b, test_train_ratio):
    """Nadeau & Bengio (2003) corrected paired t-test on per-fold scores a, b (same folds and seeds).

    test_train_ratio = mean n_test / n_train over the actual folds.
    Returns mean Δ (a − b), SD, t, two-sided p and the unadjusted 95% CI.
    """
    d = np.asarray(a, float) - np.asarray(b, float)
    n = len(d)
    mean, sd = d.mean(), d.std(ddof=1)
    se = np.sqrt((1 / n + test_train_ratio) * sd ** 2)
    if se == 0:
        t, p = (0.0, 1.0) if mean == 0 else (np.inf * np.sign(mean), 0.0)
    else:
        t = mean / se
        p = 2 * stats.t.sf(abs(t), df=n - 1)
    half = stats.t.ppf(0.975, df=n - 1) * se
    return {"mean_delta": mean, "sd": sd, "t": t, "p": p, "ci_low": mean - half, "ci_high": mean + half, "n": n}


def holm(pvalues):
    """Holm–Bonferroni adjusted p-values (monotone, capped at 1), in the input order."""
    p = np.asarray(pvalues, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[i]))
        adj[i] = running
    return adj


def decide(mean_delta, p_holm, min_delta=MIN_DELTA, alpha=ALPHA):
    """'A > B' / 'A < B' only if |Δ| >= 0.01 and Holm p < 0.05, else 'no clear difference'."""
    if abs(mean_delta) >= min_delta and p_holm < alpha:
        return "A > B" if mean_delta > 0 else "A < B"
    return "no clear difference"


def compare_family(pairs, test_train_ratio):
    """pairs: {name: (scores_a, scores_b)} for one family. Returns rows with Holm-adjusted decisions."""
    rows = [{"comparison": k, **corrected_ttest(a, b, test_train_ratio)} for k, (a, b) in pairs.items()]
    for r, ph in zip(rows, holm([r["p"] for r in rows])):
        r["p_holm"] = ph
        r["decision"] = decide(r["mean_delta"], ph)
    return rows


def kendall_tau(scores_x, scores_y):
    """Rank agreement of models between two protocols (descriptive). Inputs: {model: mean macro-F1}."""
    models = sorted(scores_x)
    res = stats.kendalltau([scores_x[m] for m in models], [scores_y[m] for m in models])
    return float(res.statistic)
