# Research Protocol

| Field | Value |
|---|---|
| Version | **1.1** (supersedes v1, commit `b14c06e`; changes listed in `amendment_log.md`, A-001) |
| Date | 2026-10-08 |
| Status | **CANDIDATE DESIGN** (v1.1 signed 2026-10-09). Under amendment A-003 the research questions and design are re-decided after the literature review (`review_protocol.md`, phase 3) and frozen as **v2.0 on 2026-10-22**, before any model is run. Until then v1.1 is the default design. |
| Schedule | 2026-10-09 → 2026-11-05: literature review 12/10–22/10, experiments and writing 23/10–05/11 |

## 1. Title (working title, final after phase 3)

A Reproducible and Leakage-Aware Evaluation of Ensemble Learning for Functional and Non-Functional Software Requirements Classification

## 2. Objective and scope

Measure, under a fixed and leakage-controlled pipeline, whether simple ensembles improve over individual classical classifiers for binary FR/NFR classification, how rule-based preprocessing affects that comparison, and how much the conclusions depend on the evaluation protocol.

In scope: binary FR vs NFR, English requirement text only, TF-IDF features, classical scikit-learn models.
Out of scope: NFR sub-classes (12-class), multi-label/mixed requirements, Transformers/LLMs, hyperparameter search, deployment.

A null result (e.g. "ensembles do not beat Linear SVM", "the gap disappears under grouped CV") is a valid outcome and will be reported as such.

## 3. Research questions (candidate; confirmed, narrowed or replaced by the gap analysis in phase 3)

- **RQ1 (individual vs ensemble).** How do individual classifiers (LR, Linear SVM, RF, Complement NB) and ensembles (Hard Voting, Stacking) compare in binary FR/NFR classification?
- **RQ2 (preprocessing).** How do minimal cleaning (P0), stopword removal (P1) and stopword removal + lemmatization (P2) affect performance and the model ranking?
- **RQ3 (evaluation protocol).** How much do performance estimates and model rankings change when (a) duplicate and near-duplicate requirements are kept in the same fold (duplicate leakage), and (b) all requirements of a project are kept in the same fold (project-level generalization)?

RQ3(a) is a leakage question. RQ3(b) is **not** called leakage: a drop under project grouping mixes project-specific vocabulary, distribution shift and class-prior shift, so it is reported as an estimate of generalization to unseen projects. The two are reported separately.

## 4. Dataset

- **Primary:** PROMISE_exp. Expected (to be verified, not assumed): 969 requirements, 444 FR / 525 NFR, columns `ProjectID`, `RequirementText`, `Class` (per Promise+, SBES 2024). Original source to trace: the paper that introduced PROMISE_exp (believed to be Lima et al., SBES 2019; verify) and the data used by Canedo & Mendes (2020).
- Raw file is stored unmodified in `data/raw/`, frozen with SHA-256 (`data/dataset_manifest.json`, `data/checksums.csv`). If the downloaded file differs from the expected description, the actual file wins and the discrepancy is recorded.
- **Label mapping:** `Class == "F"` → FR; every other class code → NFR. The list of codes actually present is reported in the audit.
- **Model input:** requirement text only. `ProjectID`, class codes and any other metadata are never used as features.
- **Not used:** the previously audited 1,145-row candidate set (354 unique descriptions).

### 4.1 Audit (before any model is trained)

N, columns, class distribution, missing/blank text, length distribution, number of projects and rows per project, exact duplicates, canonical duplicates, near-duplicate candidates, label conflicts within duplicate groups.

### 4.2 Duplicate groups (for grouping only, never for features)

1. Canonical text: Unicode NFKC → lowercase → strip → collapse whitespace → remove trailing punctuation. Identical canonical text ⇒ same group.
2. Near-duplicate candidates: character 3–5-gram TF-IDF (word-boundary analyzer) cosine similarity ≥ **0.90** between groups. Each candidate pair is reviewed manually by both members and marked `SAME` / `DIFFERENT`; only `SAME` pairs are merged (union-find). Decisions are saved in `data/processed/near_duplicate_review.csv`.
3. Labels are not used to build groups.
4. Rows with conflicting labels inside one group are **kept with their original labels** (ground truth is not edited). Their count is reported and they are listed in the error analysis.

All grouping decisions are completed and committed before the first model run.

## 5. Preprocessing (stateless, rule-based)

All variants are deterministic functions applied per text; nothing is learned from the corpus.

- **P0 minimal:** NFKC, lowercase, expand negative contractions (`won't`→`will not`, `can't`→`cannot`, `n't`→` not`), collapse whitespace.
- **P1 = P0 + stopword removal:** NLTK English stopword list minus `KEEP_WORDS`. Tokenization uses the same regex as the vectorizer (`(?u)\b\w\w+\b`).
  `KEEP_WORDS = {no, not, nor, cannot, must, shall, should, will, would, can, could, may, might, only, all, any, each, every, within, without, before, after, during, under, over, above, below, between, more, most, less, least, than, same, few, up, down, off, out, again, once}`
- **P2 = P1 + lemmatization:** POS tags from `nltk.pos_tag` computed on the P0 token sequence (before stopword removal), mapped to WordNet POS (default noun), then stopwords removed, then `WordNetLemmatizer`.
- NLTK version and resources (`stopwords`, `wordnet`, `omw-1.4`, `averaged_perceptron_tagger_eng`) are recorded in the run log.

Known interaction: removing stopwords creates bigrams across removed words; this is part of what RQ2 measures.

## 6. Features

`TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, lowercase=False, token_pattern=r"(?u)\b\w\w+\b")`, fitted on the training portion of each fold only (inside a `Pipeline`).

Optional (first to be cut): unigram-only ablation `ngram_range=(1, 1)` for the P0 setting.

## 7. Models (fixed hyperparameters, no tuning)

| ID | Model | Settings |
|---|---|---|
| M0 | `DummyClassifier` | `strategy="most_frequent"` (sanity floor) |
| M1 | `LogisticRegression` | `C=1.0, max_iter=2000` |
| M2 | `LinearSVC` | `C=1.0` |
| M3 | `RandomForestClassifier` | `n_estimators=300, random_state=seed, n_jobs=-1` |
| M4 | `ComplementNB` | `alpha=1.0` |
| M5 | Hard Voting (M1, M2, M3) | majority of 3 votes (no ties possible for 2 classes) |
| M6 | Stacking (M1, M2, M3 → LR) | see §7.1 |

Each base model inside M5/M6 has its own TF-IDF fitted on the same outer-training data.

Expectation stated in advance: M1 and M2 are highly correlated, so M5 may behave close to the better linear model. This is a hypothesis to check, not a target.

### 7.1 Stacking implementation (manual, auditable)

For each outer fold:
1. Inner 5-fold split of the outer-training rows only, using the **same splitter type as the outer protocol** (StratifiedKFold for S, StratifiedGroupKFold with the same groups for G-dup / G-proj).
2. Base models are fitted on inner-train and produce out-of-fold scores (`decision_function` for M1/M2, positive-class probability for M3).
3. Meta-learner `LogisticRegression(C=1.0)` is fitted on these OOF scores.
4. Base models are refitted on the full outer-training data; the meta-learner combines their scores on the outer-test fold.

Unit test: no outer-test index appears in any inner split. If this test is not passing by the end of week 2, M6 is dropped and the drop is recorded as an amendment.

## 8. Evaluation protocols

Five seeds: **42, 123, 2026, 3407, 9917**. Each protocol = 5 folds × 5 seeds = 25 train/test evaluations per configuration, on the same processed rows.

| ID | Splitter | Groups | Purpose |
|---|---|---|---|
| S | `StratifiedKFold(5, shuffle=True, random_state=seed)` | – | standard (comparable to literature) |
| G-dup | `StratifiedGroupKFold(5, shuffle=True, random_state=seed)` | `duplicate_group` | RQ3(a) |
| G-proj | `StratifiedGroupKFold(5, shuffle=True, random_state=seed)` | `ProjectID` | RQ3(b) |

- Invariants asserted for every fold: train ∩ test indices = ∅; for G-*: train groups ∩ test groups = ∅.
- Per-fold test size and class ratio are logged. Grouped folds may be unbalanced; this is reported, not corrected.
- **G-proj feasibility rule** (checked on the splits of all 5 seeds, before any model is trained): every test fold must contain ≥ 2 projects, ≥ 10% of the rows, and ≥ 20% of each class.
  - If the rule holds → G-proj with 5 folds.
  - If it fails with 5 folds → retry with 3 folds (same rule). Reported as such.
  - If it still fails, or `ProjectID` is missing/unreliable → G-proj is dropped and replaced by a descriptive per-project analysis (amendment). No invented grouping.
- Optional extension: leave-one-project-out for M1, M2, M5 under P0.

### 8.1 Experiment matrix

- RQ1 and RQ2: all models × {P0, P1, P2}. **Primary protocol for RQ1/RQ2 is S** (comparable to prior work); the same comparisons under G-dup are reported as a sensitivity analysis. Conclusions are written from S; any RQ1/RQ2 conclusion that flips under G-dup is stated explicitly.
- RQ3: all models × {P0, P1, P2} under **S, G-dup, G-proj**. The main RQ3 table uses **P0** (fixed in advance, not the best-performing preprocessing). The other preprocessing variants go to the appendix.

## 9. Metrics

- **Primary:** Macro-F1 over {FR, NFR}, computed **per test fold**, then averaged over the 25 folds (not pooled predictions).
- **Secondary:** accuracy, macro precision, macro recall, F1-FR, F1-NFR, confusion matrix (summed over folds, per seed).
- Prediction-level output: `row_id, project_id, duplicate_group, true_label, predicted_label, score, fold, seed, preprocessing, model, protocol`.

## 10. Decision rules (fixed before results)

Paired comparison A vs B uses the 25 paired fold scores (same folds, same seeds).

- Report mean Δ Macro-F1, SD, and a 95% CI using the **corrected repeated k-fold t-test** (Nadeau & Bengio, 2003; Bouckaert & Frank, 2004) with `n_test/n_train` taken from the actual folds.
- **"A is better than B"** only if mean Δ ≥ **0.01** AND the corrected t-test p-value is < 0.05 after Holm adjustment within the comparison family. Otherwise: "no clear difference". The unadjusted corrected 95% CI is always reported alongside.
- Comparison families (Holm is applied within each family separately):
  - **RQ1-P0, RQ1-P1, RQ1-P2** (one family per preprocessing, protocol S): M5 vs M1, M2, M3, M4 and M6 vs M1, M2, M3, M4 → 8 tests per family.
  - **RQ2** (protocol S): P1 vs P0 and P2 vs P1 for each of M1–M6 → 12 tests.
  - **RQ3-dup** and **RQ3-proj** (P0): S vs the G protocol for each of M1–M6 → 6 tests per family. Plus Kendall's τ between model rankings under S and under each G protocol (descriptive, no test).
- The 0.01 threshold is a practical-significance threshold chosen in advance, not derived from data. With ~970 rows, many comparisons are expected to end as "no clear difference"; this is reported as is.
- An RQ3 difference is called "leakage" only if the duplicate audit shows that duplicate groups cross folds under S. If there are almost no duplicates, RQ3(a) is reported as a negative finding.
- No direct superiority claims against published F1 values obtained under a different dataset version, split or F1 averaging.

## 11. Error analysis

From P0 / protocol S / seed 42: **30 misclassified rows in total**, 15 from M2 and 15 from M5, each 15 split as 8 true-NFR + 7 true-FR errors, drawn with `random_state=42` (if fewer errors exist, take all; a row misclassified by both models is counted once and replaced by the next draw). Both members label each independently with `mixed FR/NFR`, `quality keyword in FR`, `functional verb in NFR`, `ambiguous/underspecified`, `short/low context`, `possible annotation issue`, `other`. Disagreements are discussed and recorded. Ground-truth labels are never changed.

## 12. Reproducibility

- Each run logs `experiment_id, timestamp, git commit, dataset SHA-256, seed, preprocessing, model, protocol, package versions, status` in `experiments/experiment_log.csv`.
- Python 3.12 (win-amd64), pinned `requirements.txt`, scripts runnable without notebooks.
- Raw data is not pushed publicly unless its license allows redistribution.

## 13. Threats to validity (to be discussed)

Single public benchmark; binary labels hide mixed requirements; known label-quality concerns in PROMISE (Dalpiaz et al., 2019); duplicate/near-duplicate threshold choice; dependence between CV folds; uneven grouped folds; fixed (untuned) hyperparameters.

## 14. Sign-off

| Member | Role | Date | Signature |
|---|---|---|---|
| Hoang Anh (TV A) | dataset, preprocessing, splits, protocol | 2026-10-09 | Agreed (confirmed via Phat Tai) |
| Phat Tai (TV B) | literature, models, statistics, figures | 2026-10-09 | Agreed |
