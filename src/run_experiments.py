"""Run the experiment plan (protocol §8 table, A-007). Refuses to run before the protocol is LOCKED.

    python -m src.run_experiments --plan RQ1      # T-bin, M0–M6, S / G-dup / G-proj (RQ3 reuses these runs)
    python -m src.run_experiments --plan RQ2      # T-bin + T-12, M1–M5, S, NONE / IN-FOLD / BEFORE × OS-R / OS-S
    python -m src.run_experiments --plan D2       # Dalpiaz2019 replication (A-007)
"""
import argparse
import csv
import datetime
import hashlib
import importlib.metadata as md
import subprocess
import sys
import uuid

import pandas as pd

from src.data import ROOT
from src.experiment import run_config
from src.splits import SEEDS, make_folds

PROTOCOL = ROOT / "protocol/research_protocol.md"
PROCESSED = ROOT / "data/processed"
OUT = ROOT / "results"


def protocol_locked(path=PROTOCOL):
    return any(line.startswith("| Status | **LOCKED**") for line in path.read_text(encoding="utf-8").splitlines())


def plan(name):
    """Yield (dataset_file, task, model, protocol, condition, oversampler)."""
    if name == "RQ1":
        for m in ("M0", "M1", "M2", "M3", "M4", "M5", "M6"):
            for p in ("S", "G-dup", "G-proj"):
                yield "requirements.csv", "T-bin", m, p, "NONE", None
    elif name == "RQ2":
        for task in ("T-bin", "T-12"):
            for m in ("M1", "M2", "M3", "M4", "M5"):
                yield "requirements.csv", task, m, "S", "NONE", None
                for c in ("IN-FOLD", "BEFORE"):
                    for o in ("OS-R", "OS-S"):
                        yield "requirements.csv", task, m, "S", c, o
    elif name == "D2":
        for m in ("M1", "M2", "M3", "M4", "M5"):
            for p in ("S", "LODO"):
                yield "dalpiaz_requirements.csv", "T-bin", m, p, "NONE", None
            for c in ("IN-FOLD", "BEFORE"):
                for o in ("OS-R", "OS-S"):
                    yield "dalpiaz_requirements.csv", "T-bin", m, "S", c, o
            yield "dalpiaz_requirements_noboth.csv", "T-bin", m, "S", "NONE", None
    else:
        raise SystemExit(f"Unknown plan {name!r}")


def _git_commit():
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_splits(df, dataset, protocols, n_splits=5):
    rows = []
    for p in protocols:
        for seed in ([0] if p == "LODO" else SEEDS):
            for k, (_, te) in enumerate(make_folds(df, p, seed, n_splits)):
                rows += [{"dataset": dataset, "protocol": p, "seed": seed, "row_id": r, "fold": k}
                         for r in df["requirement_id"].iloc[te]]
    return pd.DataFrame(rows)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, choices=["RQ1", "RQ2", "D2"])
    ap.add_argument("--owner", default="phat-tai")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    if not protocol_locked():
        raise SystemExit("Protocol is not LOCKED (research_protocol.md §14). No model is run before LOCKED.")

    jobs = list(plan(args.plan))
    data = {f: pd.read_csv(PROCESSED / f, keep_default_na=False) for f in {j[0] for j in jobs}}
    for f, df in data.items():
        df["duplicate_group"] = df["duplicate_group"].astype(int)
    for d in ("tables", "predictions", "splits"):
        (OUT / d).mkdir(parents=True, exist_ok=True)

    split_tables = [save_splits(df, f, sorted({j[3] for j in jobs if j[0] == f})) for f, df in data.items()]
    pd.concat(split_tables).to_csv(OUT / "splits" / f"splits_{args.plan}.csv", index=False)

    folds, preds = [], []
    for i, (f, task, m, p, c, o) in enumerate(jobs, 1):
        for seed in ([0] if p == "LODO" else SEEDS):
            fr, pr = run_config(data[f], task, m, p, c, o, seed)
            fr.insert(0, "dataset", f)
            pr.insert(0, "dataset", f)
            folds.append(fr)
            preds.append(pr)
        print(f"[{i}/{len(jobs)}] {f} {task} {m} {p} {c} {o or ''}: macro-F1 {folds[-1].macro_f1.mean():.3f} (last seed)")

    pd.concat(folds).to_csv(OUT / "tables" / f"fold_scores_{args.plan}.csv", index=False)
    pd.concat(preds).to_csv(OUT / "predictions" / f"predictions_{args.plan}.csv", index=False)

    raw = ROOT / "data/raw"
    shas = ";".join(f"{p.relative_to(raw).as_posix()}={_sha(p)[:12]}" for p in sorted(raw.rglob("*"))
                    if p.suffix in (".arff", ".csv"))
    versions = ";".join(f"{pkg}={md.version(pkg)}" for pkg in ("scikit-learn", "imbalanced-learn", "numpy", "pandas"))
    with open(ROOT / "experiments/experiment_log.csv", "a", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow([
            uuid.uuid4().hex[:8], datetime.datetime.now().isoformat(timespec="seconds"), args.owner, _git_commit(),
            shas, args.plan, "P0", "tfidf(1,2) min_df=2", "see fold_scores", "|".join(map(str, SEEDS)),
            "done", f"results/tables/fold_scores_{args.plan}.csv", versions])
    print("Saved results/tables, results/predictions, results/splits; logged to experiments/experiment_log.csv")


if __name__ == "__main__":
    main()
