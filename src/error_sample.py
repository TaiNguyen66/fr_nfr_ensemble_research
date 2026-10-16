"""Protocol §11 error-analysis sample: T-bin, G-dup, seed 42; 15 misclassified rows each from M2 and M5
(8 true-NFR + 7 true-FR), shuffled with random_state=42. A row already drawn for M2 is skipped when drawing for M5
(counted once, replaced by the next draw).

    python -m src.error_sample

Writes results/predictions/error_analysis_sample.csv (gitignored: contains requirement text) with empty label columns.
"""
import pandas as pd

from src.data import ROOT

SEED, PER_CLASS = 42, {"NFR": 8, "FR": 7}
CATEGORIES = ["mixed FR/NFR", "quality keyword in FR", "functional verb in NFR", "ambiguous/underspecified",
              "short/low context", "possible annotation issue", "other"]


def draw(errors, taken):
    picked = []
    for label, n in PER_CLASS.items():
        pool = errors[(errors.true_label == label) & ~errors.row_id.isin(taken)]
        picked.append(pool.sample(frac=1, random_state=SEED).head(n))
    return pd.concat(picked)


def main():
    pred = pd.read_csv(ROOT / "results/predictions/predictions_RQ1.csv", keep_default_na=False)
    pred = pred[(pred.task == "T-bin") & (pred.protocol == "G-dup") & (pred.seed == SEED)]
    text = pd.read_csv(ROOT / "data/processed/requirements.csv", keep_default_na=False)
    text = text[["requirement_id", "text", "label_12"]].rename(columns={"requirement_id": "row_id"})
    parts, taken = [], set()
    for model in ("M2", "M5"):
        p = pred[pred.model == model]
        errors = p[p.true_label != p.predicted_label].sort_values("row_id")
        sample = draw(errors, taken)
        taken |= set(sample.row_id)
        short = {l: (sample.true_label == l).sum() for l in PER_CLASS}
        print(f"{model}: {len(errors)} errors, drew {len(sample)} {short}")
        parts.append(sample.assign(model=model))
    out = pd.concat(parts).merge(text, on="row_id", how="left")
    out = out[["model", "row_id", "text", "label_12", "true_label", "predicted_label", "fold"]]
    for c in ("phat_tai_category", "hoang_anh_category", "reconciled_category", "note"):
        out[c] = ""
    path = ROOT / "results/predictions/error_analysis_sample.csv"
    out.to_csv(path, index=False, encoding="utf-8")
    print(f"Saved {path.relative_to(ROOT)}; categories: {' | '.join(CATEGORIES)}")


if __name__ == "__main__":
    main()
