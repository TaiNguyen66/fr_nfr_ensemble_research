# Running the experiments

This guide reproduces the results of the study from the raw datasets. Commands are written for PowerShell on Windows (Python 3.12). On Linux or macOS, replace the activation line with `source .venv/bin/activate` and the path separators accordingly.

## 1. Set up

```powershell
git clone https://github.com/TaiNguyen66/fr_nfr_ensemble_research.git
cd fr_nfr_ensemble_research
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Package versions are pinned in `requirements.txt`. The reported results were produced with these versions.

## 2. Get the raw data

The raw files are not in this repository (see [`data/README.md`](data/README.md)).

| File | Source |
|---|---|
| `data/raw/PROMISE_exp.arff` | <https://github.com/AleksandarMitrevski/se-requirements-classification/tree/master/0-datasets/PROMISE_exp> (public mirror of the data of Lima et al. 2019) |
| `data/raw/dalpiaz2019/dronology.csv`, `leeds.csv`, `reqview.csv`, `wasp.csv` | <https://zenodo.org/records/3309582>: download `RE2019-Paper96.zip` and take the files from `Manually tagged datasets/` |

Do not open these files in a spreadsheet program and save them again, because that changes their bytes and their hash.

Check that you have the same files as the study:

```powershell
Get-FileHash data\raw\PROMISE_exp.arff -Algorithm SHA256
Get-ChildItem data\raw\dalpiaz2019\*.csv | Get-FileHash -Algorithm SHA256
```

Compare the hashes with the `sha256` column of `data/checksums.csv`. If any hash differs, stop: the results will not match.

## 3. Check the code and build the processed data

```powershell
python -m pytest -q tests
python -m src.audit_dataset
```

All 37 tests should pass. `audit_dataset` writes three files to `data/processed/` (they contain requirement text and are ignored by git) and should print:

```text
PROMISE_exp: 969 rows, 47 projects, {'NFR': 525, 'FR': 444}, 12 classes
  near-duplicate candidates >= 0.9: 14; SAME merged: 5
  duplicate groups with > 1 row: 8 (16 rows); label conflicts (bin): 0
  groups crossing folds under S (5 seeds): [6, 7, 8, 7, 6]
Dalpiaz2019: 327 rows, {'FR': 187, 'NFR': 140}, duplicate rows: 0
Dalpiaz2019 (no both): 246 rows, {'FR': 187, 'NFR': 59}, duplicate rows: 0
```

The near-duplicate decisions it uses are in `data/processed/near_duplicate_review.csv` (tracked).

## 4. Run the experiments

`src.run_experiments` refuses to run unless `protocol/research_protocol.md` is marked LOCKED, which it is in this repository.

| Command | Question | Data | Configurations | Fold fits |
|---|---|---|---|---|
| `python -m src.run_experiments --plan RQ1` | RQ1 and RQ3 | PROMISE_exp, T-bin: 7 models × 3 protocols (S, G-dup, G-proj) | 21 | 525 |
| `python -m src.run_experiments --plan RQ2` | RQ2 | PROMISE_exp, T-bin and T-12: 5 models × 5 oversampling conditions | 50 | 1250 |
| `python -m src.run_experiments --plan D2` | Replication | Dalpiaz et al. data, T-bin | 35 | 770 |

Each configuration runs 5 seeds (42, 123, 2026, 3407, 9917) of 5-fold CV, giving 25 fold scores; leave-one-dataset-out (LODO) on the Dalpiaz data is a single run with 4 folds. Run the plans in the order RQ1, RQ2, D2. RQ1 is the fastest and is a good first check. RQ2 takes the longest (random forest and voting on 12 classes, plus SMOTE).

To keep a log of the screen output:

```powershell
New-Item -ItemType Directory -Force logs | Out-Null
python -m src.run_experiments --plan RQ1 *>&1 | Tee-Object logs\run_RQ1.txt
```

`--owner` sets the name written to `experiments/experiment_log.csv` (default `phat-tai`). The progress lines have the form

```text
[3/21] requirements.csv T-bin M0 G-proj NONE : macro-F1 0.351 (last seed)
```

(configuration number, data file, task, model, protocol, oversampling condition, macro-F1 of the last seed). The value shown is for monitoring only.

Results are written only when a whole plan has finished. If a run is interrupted, run the same command again. The seeds are fixed, so the output is identical. Re-running a plan overwrites its files in `results/`, while `experiments/experiment_log.csv` only gains a line.

## 5. Outputs

| File | Content |
|---|---|
| `results/tables/fold_scores_<PLAN>.csv` | One row per fold: macro-F1, accuracy, macro precision, macro recall, sizes, seed, fold |
| `results/splits/splits_<PLAN>.csv` | Which row is in which fold, for every protocol and seed |
| `results/predictions/predictions_<PLAN>.csv` | Per-row predictions (not tracked by git) |
| `experiments/experiment_log.csv` | One line per run: run id, time, commit, dataset hashes, plan, seeds, package versions |

A quick look at the mean macro-F1 per configuration (the `count` column should be 25, or 4 for LODO):

```powershell
python -c "import pandas as pd; d=pd.read_csv('results/tables/fold_scores_RQ1.csv'); print(d.groupby(['task','model','protocol','condition','oversampler'],dropna=False).macro_f1.agg(['mean','std','count']).round(3).to_string())"
```

These means are descriptive. Claims that one model beats another come only from the corrected repeated k-fold t-test with Holm adjustment (protocol §10), computed in the next step.

## 6. Analyse the results

```powershell
python -m src.analyze_results            # add --no-figures to skip the plots
python -m src.paper_tables               # LaTeX tables and summary figure
```

`analyze_results` writes to `results/tables/` and `results/figures/`:

- `stats_<family>.csv` for RQ3 under G-dup and S: mean paired difference, SD, t, p, 95% interval, Holm-adjusted p and the decision (|Δ| ≥ 0.01 and adjusted p < 0.05).
- `descriptive_<family>.csv` for RQ1(a), RQ1(b), RQ2 and the replication: mean and SD of each side and Δ as the difference of the two means. There is no p-value, because the two sides use different test folds (amendment A-009).
- `summary_<plan>.csv`, `descriptive_none_vs_infold_<plan>.csv`, `descriptive_RQ1-D2_S_vs_LODO.csv` and `kendall_tau.csv` (agreement between model rankings).

`paper_tables` writes the LaTeX tables and the summary figure used in the paper to `results/paper_tables/`.

## 7. Check that you reproduce the reported numbers

A complete re-run on 2026-10-18 reproduced every fold score bit for bit. To compare your run with the committed files, hash your `results/tables/fold_scores_*.csv` and compare them with the files in this repository (`git status` shows any difference). A difference means that the data, the package versions or the code differ from the study. Do not change models, parameters, metrics, splits or data to improve a result; any change to the design is recorded as an amendment in `protocol/amendment_log.md`.

If you see an error like `AssertionError: ... in both train and test`, a leakage check has stopped the run. Report it with your log instead of working around it. A `ConvergenceWarning` from the linear SVM is common and not an error.
