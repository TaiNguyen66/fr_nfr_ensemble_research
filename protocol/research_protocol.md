# Research Protocol

| Field | Value |
|---|---|
| Version | **2.0** (supersedes v1.1; derived from the gap analysis `literature/review/gap_analysis.md`; changes in `amendment_log.md`, A-005) |
| Date | 2026-10-14 |
| Status | **LOCKED** on 2026-10-16 (signed by the lead, Phat Tai, A-008). No model is run before LOCKED. Any later change = new amendment entry approved by the lead (A-008). |
| Schedule | Experiments and writing 2026-10-18 → 2026-11-05 |

## 1. Title

How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification? A Leakage-Aware Re-Evaluation of Single and Ensemble Classifiers

(Final title may be shortened for the venue; the content below does not depend on it.)

## 2. Objective and scope

The literature review (21 empirical papers, verified by both members) found that **14/21 studies split train/test at random without handling duplicate requirements, 0/21 keep duplicates in the same fold, 3 of the 6 studies that oversample do so before splitting, and 4/6 ensemble studies claim improvements without a statistical test**. No study quantifies how much these practices inflate reported performance for FR/NFR classification.

This study measures, on a public benchmark and with a fixed pipeline: (1) how much performance and model rankings change when duplicate requirements or projects are kept within one fold; (2) how much oversampling before splitting inflates estimates; (3) whether ensembles still outperform single classifiers once evaluation is leakage-aware and differences are tested.

In scope: English requirement text, TF-IDF features, classical scikit-learn models and simple ensembles, binary FR/NFR (all RQs) and 12-class (RQ2 only).
Out of scope: Transformers/LLMs, hyperparameter search, preprocessing comparison (dropped: already studied by Abad et al. 2017), multi-label/mixed requirements, deployment.

A null result (e.g. "no measurable inflation", "ensembles do not beat Linear SVM") is a valid outcome and will be reported as such.

## 3. Research questions

| RQ | Question | Gap (review) |
|---|---|---|
| **RQ1** | How much do performance estimates and model rankings change when (a) duplicate / near-duplicate requirements are kept in the same fold, and (b) all requirements of a project are kept in the same fold, compared with random stratified CV? | G1, G5 |
| **RQ2** | How much does oversampling the whole dataset **before** splitting inflate performance estimates compared with oversampling only the training part of each fold? | G2 |
| **RQ3** | Under leakage-aware evaluation, do Hard Voting and Stacking outperform the individual classifiers (LR, Linear SVM, RF, Complement NB) by a practically and statistically meaningful margin? | G3 |

RQ1(a) and RQ2 are leakage questions. RQ1(b) is **not** called leakage: a drop under project grouping mixes project-specific vocabulary, distribution shift and class-prior shift, and is reported as an estimate of generalization to unseen projects.

G4 (inconsistent F1 reporting) and G6 (reproducibility) are addressed as methodological contributions: every result reports macro-F1 and per-class F1; data hashes, code and splits are published.

## 4. Dataset

- **Primary:** PROMISE_exp. Expected (to be verified, not assumed): 969 requirements, 444 FR / 525 NFR, 12 class codes, columns `ProjectID`, `RequirementText`, `Class`. Source, version, license and SHA-256 are recorded in `data/README.md` and `data/dataset_manifest.json`. If the downloaded file differs from the expected description, the actual file wins and the discrepancy is recorded.
- Raw file stored unmodified in `data/raw/`; frozen with `scripts/freeze_dataset.py`.
- **Tasks:**
  - **T-bin:** `Class == "F"` → FR, every other code → NFR. Used by RQ1, RQ2, RQ3.
  - **T-12:** the 12 original class codes. Used by RQ2 only (strong imbalance; the setting where the reviewed studies oversampled).
- **Model input:** requirement text only. `ProjectID`, class codes and any other metadata are never used as features.

### 4.1 Audit (before any model is trained)

N, columns, class distribution (T-bin and T-12), missing/blank text, length distribution, number of projects and rows per project, exact duplicates, canonical duplicates, near-duplicate candidates, label conflicts within duplicate groups, and **how many duplicate groups would cross folds under protocol S** (needed to interpret RQ1(a)).

### 4.2 Duplicate groups (for grouping only, never for features)

1. Canonical text: Unicode NFKC → lowercase → strip → collapse whitespace → remove trailing punctuation. Identical canonical text ⇒ same group.
2. Near-duplicate candidates: character 3–5-gram TF-IDF (word-boundary analyzer) cosine similarity ≥ **0.90** between groups. Each candidate pair is reviewed manually by both members (`SAME` / `DIFFERENT`); only `SAME` pairs are merged (union-find). Decisions saved in `data/processed/near_duplicate_review.csv`.
3. Labels are not used to build groups.
4. Rows with conflicting labels inside one group are **kept with their original labels**; their count is reported.

All grouping decisions are committed before the first model run.

## 5. Preprocessing (fixed)

One stateless, rule-based variant for all experiments (**P0**): Unicode NFKC, lowercase, expand negative contractions (`won't`→`will not`, `can't`→`cannot`, `n't`→` not`), collapse whitespace. No stopword removal, no lemmatization. (The preprocessing comparison of v1.1 is dropped; reason in A-005.)

## 6. Features

`TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, lowercase=False, token_pattern=r"(?u)\b\w\w+\b")`, fitted on the training portion of each fold only (inside a `Pipeline`).

## 7. Models (fixed hyperparameters, no tuning)

| ID | Model | Settings | Used in |
|---|---|---|---|
| M0 | `DummyClassifier` | `strategy="most_frequent"` (sanity floor) | RQ1, RQ3 |
| M1 | `LogisticRegression` | `C=1.0, max_iter=2000` | all |
| M2 | `LinearSVC` | `C=1.0` | all |
| M3 | `RandomForestClassifier` | `n_estimators=300, random_state=seed, n_jobs=-1` | all |
| M4 | `ComplementNB` | `alpha=1.0` | all |
| M5 | Hard Voting (M1, M2, M3) | majority vote (T-12: ties broken by M2's prediction) | all |
| M6 | Stacking (M1, M2, M3 → LR) | see §7.1 | RQ1, RQ3 |

Each base model inside M5/M6 has its own TF-IDF fitted on the same outer-training data. Expectation stated in advance: M1 and M2 are highly correlated, so M5 may behave close to the better linear model.

### 7.1 Stacking (manual, auditable)

For each outer fold: (1) inner 5-fold split of the outer-training rows only, with the **same splitter type as the outer protocol** (StratifiedKFold for S, StratifiedGroupKFold with the same groups for G-dup / G-proj); (2) base models fitted on inner-train produce out-of-fold scores (`decision_function` for M1/M2, positive-class probability for M3); (3) meta-learner `LogisticRegression(C=1.0)` fitted on these scores; (4) base models refitted on the full outer-training data, meta-learner applied to the outer-test fold.

Unit test: no outer-test index appears in any inner split. If not passing by 2026-10-22 (gate G4), M6 is dropped (amendment) and M5 is the only ensemble.

### 7.2 Oversampling conditions (RQ2)

Oversamplers (`imbalanced-learn`): **OS-R** `RandomOverSampler(random_state=seed)` (duplicates minority rows; reproduces what the reviewed studies did) and **OS-S** `SMOTE(random_state=seed, k_neighbors=min(5, n_min-1))` applied to TF-IDF vectors.

| Condition | What is oversampled | Leakage |
|---|---|---|
| **NONE** | nothing | – (reference) |
| **IN-FOLD** | training part of each fold only (inside the pipeline, after TF-IDF) | no |
| **BEFORE** | the whole dataset, then split (OS-R: duplicated rows; OS-S: TF-IDF fitted on all rows, synthetic vectors generated, then split) | yes, by construction |

In BEFORE, the test fold is drawn from the oversampled set, as in the reviewed studies; metrics are computed on that test fold. In IN-FOLD and NONE, test folds contain only original rows. The difference BEFORE − IN-FOLD is the quantity of interest.

## 8. Evaluation protocols

Five seeds: **42, 123, 2026, 3407, 9917**. Each protocol = 5 folds × 5 seeds = 25 train/test evaluations per configuration.

| ID | Splitter | Groups | Purpose |
|---|---|---|---|
| S | `StratifiedKFold(5, shuffle=True, random_state=seed)` | – | as in most reviewed studies |
| G-dup | `StratifiedGroupKFold(5, shuffle=True, random_state=seed)` | `duplicate_group` | RQ1(a); **primary protocol for RQ3** |
| G-proj | `StratifiedGroupKFold(5, shuffle=True, random_state=seed)` | `ProjectID` | RQ1(b) |

- Invariants asserted for every fold: train ∩ test indices = ∅; for G-*: train groups ∩ test groups = ∅.
- Per-fold test size and class ratio are logged; uneven grouped folds are reported, not corrected.
- **G-proj feasibility rule** (checked on all 5 seeds before any model is trained): every test fold has ≥ 2 projects, ≥ 10% of rows and ≥ 20% of each class (T-bin). Fails with 5 folds → retry with 3 folds. Still fails or `ProjectID` unreliable → RQ1(b) is dropped and replaced by a descriptive per-project analysis (amendment).

### 8.1 Experiment matrix

| RQ | Task | Models | Protocols | Oversampling | Configurations × 25 runs |
|---|---|---|---|---|---|
| RQ1 | T-bin | M0–M6 | S, G-dup, G-proj | NONE | 21 |
| RQ2 | T-bin, T-12 | M1–M5 | S | NONE, IN-FOLD, BEFORE × {OS-R, OS-S} | 2 tasks × 5 models × 5 = 50 |
| RQ3 | T-bin | M0–M6 | G-dup (primary); S and G-proj reported alongside | NONE | (reuses RQ1 runs) |

The whole matrix is run **once**, after gate G4. A bug fix means re-running the whole matrix.

## 9. Metrics

- **Primary:** macro-F1 (over FR/NFR for T-bin; over the 12 classes for T-12), computed **per test fold**, then averaged over the 25 folds.
- **Secondary:** accuracy, macro precision, macro recall, per-class F1, confusion matrix (summed over folds, per seed).
- Prediction-level output: `row_id, project_id, duplicate_group, true_label, predicted_label, score, fold, seed, task, model, protocol, oversampling`.

## 10. Decision rules (fixed before results)

> **A-009 (2026-10-25):** RQ1-dup, RQ1-proj, RQ2-bin, RQ2-12 and the Dalpiaz BEFORE vs IN-FOLD family are reported descriptively only (different test folds cannot be paired). The test and decision rule below now apply to RQ3 only. Text below is kept as locked on 2026-10-16.

Paired comparison A vs B uses the 25 paired fold scores (same folds, same seeds).

- Report mean Δ macro-F1, SD, and a 95% CI from the **corrected repeated k-fold t-test** (Nadeau & Bengio, 2003; Bouckaert & Frank, 2004) with `n_test/n_train` taken from the actual folds.
- **"A differs from / is better than B"** only if |mean Δ| ≥ **0.01** AND the corrected p-value < 0.05 after Holm adjustment within the family. Otherwise "no clear difference". The unadjusted CI is always reported.
- Comparison families (Holm within each):
  - **RQ1-dup:** S vs G-dup for each of M1–M6 → 6 tests. **RQ1-proj:** S vs G-proj for M1–M6 → 6 tests. Plus Kendall's τ between model rankings (S vs each G protocol), descriptive.
  - **RQ2-bin** and **RQ2-12:** BEFORE vs IN-FOLD for each model × oversampler (5 × 2) → 10 tests per task. NONE vs IN-FOLD reported descriptively.
  - **RQ3 (G-dup):** M5 vs M1–M4 and M6 vs M1–M4 → 8 tests. The same 8 comparisons under S are reported to show whether the conclusion changes with the protocol.
- "Leakage" wording for RQ1(a) is used only if the audit shows that duplicate groups actually cross folds under S. If there are almost no duplicates, RQ1(a) is reported as a negative finding.
- No superiority claims against published numbers obtained with another dataset version, split or F1 averaging.

## 11. Error analysis

From T-bin / protocol G-dup / seed 42: 30 misclassified rows, 15 from M2 and 15 from M5 (each 8 true-NFR + 7 true-FR), drawn with `random_state=42`; a row misclassified by both models is counted once and replaced by the next draw. Both members label each independently (`mixed FR/NFR`, `quality keyword in FR`, `functional verb in NFR`, `ambiguous/underspecified`, `short/low context`, `possible annotation issue`, `other`), then reconcile. Ground-truth labels are never changed.

## 12. Reproducibility

- Each run logs `experiment_id, timestamp, git commit, dataset SHA-256, seed, task, model, protocol, oversampling, package versions, status` in `experiments/experiment_log.csv`.
- Python 3.12 (win-amd64), pinned `requirements.txt` (adds `imbalanced-learn`), scripts runnable without notebooks; split indices saved.
- Raw data is not pushed publicly unless its license allows redistribution.

## 13. Threats to validity (to be discussed)

Single public benchmark; binary labels hide mixed requirements; label-quality concerns in PROMISE (Dalpiaz et al., 2019); near-duplicate threshold; dependence between CV folds; uneven grouped folds; fixed hyperparameters; RQ2 reproduces the BEFORE practice in a simplified form (not each paper's exact pipeline); the literature review only covers open-access papers downloadable automatically (A-004).

## 14. Sign-off

| Member | Role | Date | Signature |
|---|---|---|---|
| Hoang Anh (TV A) | advisory; writes sections on request (A-008) | — | Not required (A-008) |
| Phat Tai (TV B) | lead; literature, models, statistics, figures | 2026-10-16 | Signed: protocol LOCKED (A-008) |
