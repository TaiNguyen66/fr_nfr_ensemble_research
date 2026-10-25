# Fact sheet (single source of truth for writing the paper and slides)

Every number in the paper must come from this file or from `tables/*.tex`. If something is not here, do not write it; ask Phat Tai.
Source of all results: `results/tables/*.csv` (first run 2026-10-16, re-run 2026-10-18 bit-identical).

## 1. Title and research questions

**Title:** How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification? A Leakage-Aware Re-Evaluation of Single and Ensemble Classifiers

- **RQ1** How much do performance estimates and model rankings change when (a) duplicate / near-duplicate requirements are kept in the same fold (G-dup), and (b) all requirements of a project are kept in the same fold (G-proj), compared with random stratified CV (S)?
- **RQ2** How much does oversampling the whole dataset **before** splitting inflate performance estimates compared with oversampling only the training part of each fold (IN-FOLD)?
- **RQ3** Under leakage-aware evaluation (G-dup), do Hard Voting (M5) and Stacking (M6) outperform the individual classifiers M1–M4 by a practically and statistically meaningful margin?

Only RQ1(a) and RQ2 are *leakage* questions. RQ1(b) is about **generalization to unseen projects** (project vocabulary, distribution shift, class-prior shift), not leakage.

## 2. Motivation: literature review (our own systematic selection)

- 30 papers in the final set; after verification by both authors, **21 empirical FR/NFR classification studies** are counted (1 background paper on code duplication, `allamanis2019adverse`, is not counted).
- Gaps found in the 21 studies:

| Gap | Finding | Example keys |
|---|---|---|
| G1 random split, no duplicate handling | **14/21** split at random without handling duplicates; **0/21** keep duplicates in one fold | `toth2019comparative`, `rahman2023functional`, `li2025study`, `abad2017what`, `kiani2026deep`, `khayashi2026deep`, `rahimi2021phase`, `baskoro2021systematic`, `kadhim2026enhancing`, `eltahier2025bert`, `metu2024hybrid`, `binkhonain2025prompts`, `or2025improving`, `abbas2024classification` |
| G2 oversampling before split | **3 of the 6** studies that oversample do it before splitting | `kiani2026deep`, `baskoro2021systematic`, `metu2024hybrid` (before); `hey2020norbert`, `rahimi2021phase`, `or2025improving` (in training data only) |
| G3 ensemble claims untested | **4/6** ensemble studies claim improvements without a statistical test | ensembles: `rahimi2020ensemble`, `rahimi2021phase`, `abbas2024classification`, `metu2024hybrid`, `kiani2026deep`, `kadhim2026enhancing` (tested: `kiani2026deep`, `kadhim2026enhancing`) |
| G4 metric reporting | only **1/21** report macro-F1 | `binkhonain2025prompts` |
| G5 project-level evaluation | **3/21** evaluate on unseen projects/domains, plus NoRBERT partly (leave-one-project-out) | `tahir2025cross`, `ali2025multi`, `martin2025evaluating`; partly `hey2020norbert` |
| G6 reproducibility | **5/21** publish code and data | `tahir2025cross`, `hey2020norbert`, `alhoshan2023zero`, `eltahier2025bert`, `martin2025evaluating` |

- The two highest scores in the set (98.79% accuracy, `metu2024hybrid`; 99%, `baskoro2021systematic`) both show signs of oversampling before splitting. Studies that evaluate on unseen projects report clearly lower scores (e.g. F1 0.62 in `martin2025evaluating`). This is an observation, **not** proof that those papers are wrong.
- Duplication inflating ML results is documented for source code (up to 100% inflation, `allamanis2019adverse`) and for ML-based science in general (`kaufman2012`, `kapoor2023`); it has not been quantified for FR/NFR classification.
- Limitation of the review: only open-access papers whose PDF downloaded automatically were included.

## 3. Data

| | PROMISE_exp (primary) | Dalpiaz et al. (replication) |
|---|---|---|
| Source | `lima2019` (expands PROMISE NFR, `clelandhuang2007`); GitHub mirror, SHA-256 recorded | `dalpiaz2019`, data `dalpiaz2019data` (Zenodo, GPL-3.0): dronology, leeds, reqview, wasp |
| Rows | 969 (444 FR / 525 NFR) | 327 (187 FR / 140 NFR) |
| Classes | 12 codes: F 444, SE 125, US 85, O 77, PE 67, LF 49, A 31, MN 24, SC 22, FT 18, L 15, PO 12 | binary only |
| Projects | 47 (1–92 rows each) | 4 datasets |
| Duplicates | 3 exact-duplicate groups; 14 near-duplicate candidates (char 3–5-gram TF-IDF cosine ≥ 0.90), 5 confirmed SAME → **8 duplicate groups, 16 rows**, 0 label conflicts. Under S, 6–8 groups cross folds (per seed) | 0 duplicates, 0 overlap with PROMISE_exp |
| Label mapping | T-bin: `F` → FR, all other codes → NFR | IsQuality = 1 → NFR (incl. 81 rows that are both F and Q); only IsFunctional = 1 → FR; 4 unlabeled rows dropped |
| Sensitivity | — | "no-both": drop the 81 both-labelled rows → 246 rows (187 FR / 59 NFR), only under S |

Raw PROMISE_exp is not redistributed (license unknown).

## 4. Pipeline (fixed in advance, no tuning)

- Preprocessing P0: Unicode NFKC, lowercase, expand negative contractions, collapse whitespace. No stop-word removal, no lemmatization.
- Features: TF-IDF word uni+bigrams, `min_df=2`, sublinear tf, **fitted on the training fold only** (inside a pipeline).
- Models (scikit-learn `pedregosa2011`, default-like fixed hyperparameters):
  - M0 Dummy (most frequent) — sanity floor
  - M1 Logistic Regression (C=1)
  - M2 Linear SVM (C=1)
  - M3 Random Forest (300 trees)
  - M4 Complement Naive Bayes (alpha=1)
  - M5 Hard Voting of M1, M2, M3
  - M6 Stacking of M1, M2, M3 with a logistic-regression meta-learner; inner 5-fold CV on the outer training rows only, using the same splitter type as the outer protocol (unit-tested: no outer-test row enters inner training).
- Oversamplers (imbalanced-learn `lemaitre2017`): OS-R random oversampling; OS-S SMOTE (`chawla2002`) on TF-IDF vectors.
- Conditions: NONE; IN-FOLD (oversample training fold only, test folds contain original rows only); BEFORE (oversample the whole dataset, then split; for OS-S TF-IDF is fitted on all rows; test folds come from the oversampled set, as in the reviewed studies).
- Protocols: S = StratifiedKFold(5); G-dup = StratifiedGroupKFold(5) on duplicate groups; G-proj = StratifiedGroupKFold(5) on ProjectID; LODO = leave-one-dataset-out (Dalpiaz only, 4 folds).
- Repetition: 5 seeds (42, 123, 2026, 3407, 9917) × 5 folds = **25 paired scores** per configuration. Test fold sizes: S and G-dup 193–194 rows; G-proj 172–245 rows.
- Runs: RQ1 21 configurations (525 fold fits), RQ2 50 configurations (1250), Dalpiaz 35 configurations (770).

## 5. Statistics and wording rules (protocol §10, amended by A-009 on 2026-10-25)

- **A-009:** comparisons across protocols (S vs G-dup, S vs G-proj) and across oversampling conditions (BEFORE vs IN-FOLD, PROMISE_exp and Dalpiaz) are **descriptive only**: their test folds are different rows (S vs G-dup/G-proj: 0/25 identical folds, ~20% shared rows; BEFORE folds 210–1066 rows vs 193–194), so no paired test, p-value, CI or "clear difference" label. Report mean ± SD per side and Δ = difference of means. The paired test below applies to **RQ3 only**. No model was re-run.

- Primary metric: **macro-F1**, computed per test fold, averaged over 25 folds. Secondary: accuracy, macro precision, macro recall.
- Paired comparison A vs B (RQ3 only): mean Δ, SD, 95% CI from the **corrected repeated k-fold t-test** (`nadeau2003`, `bouckaert2004`), with the real n_test/n_train ratio.
- **Clear difference** only if |mean Δ| ≥ 0.01 **and** Holm-adjusted p < 0.05 (`holm1979`) within the family. Otherwise write "**no clear difference**" (not "equal", not "slightly better").
- Tested families: RQ3 under G-dup (8) and under S (8). Descriptive: RQ1-dup (6), RQ1-proj (6), RQ2-bin (10), RQ2-12 (10), Dalpiaz BEFORE vs IN-FOLD (10), S vs LODO, Kendall τ, NONE vs IN-FOLD, no-both.
- Do **not** call RQ1(a) "leakage" (too few duplicates). Do **not** call RQ1(b) "leakage". Do **not** claim superiority over published numbers (different data versions, splits, F1 averaging).
- Protocol was locked on 2026-10-16 before any model was run; no configuration was re-run to change results; negative results are reported.

## 6. Results (macro-F1)

### RQ1 (Table `tab:rq1`)
- **(a) S vs G-dup: |Δ| < 0.01 for every model (descriptive).** Δ from −0.003 to +0.005; fold SD 0.018–0.031 (S), 0.018–0.025 (G-dup). Rankings: Kendall τ = 0.733.
  - Interpretation: PROMISE_exp has only 8 duplicate groups (16 of 969 rows), so duplicate leakage cannot have a large effect *on this dataset*. A negative finding, not proof that duplicates never matter.
- **(b) S vs G-proj: drop for all six models (descriptive).** Δ = +0.134 (M4) to +0.190 (M3). G-proj macro-F1 0.661–0.755 vs S 0.851–0.893. Fold SD under G-proj 0.052–0.113 (vs 0.018–0.031 under S). Kendall τ (S vs G-proj) = 0.600: rankings change.
  - Best under S: M2 (0.893); best under G-proj: M4 (0.755).
- M0 (dummy) ≈ 0.35 under every protocol (sanity check passed).

### RQ2 (Table `tab:rq2`, protocol S, models M1–M5, OS-R and OS-S)
- **T-bin (FR vs NFR): small, consistent increase (descriptive).** BEFORE − IN-FOLD = +0.015 to +0.027 (all positive), same order as fold SD (0.015–0.032). BEFORE 0.878–0.920 vs IN-FOLD 0.855–0.894.
- **T-12 (12 classes): large inflation for all ten (descriptive).** BEFORE − IN-FOLD = **+0.392 to +0.491**; fold SD 0.002–0.006 (BEFORE), 0.040–0.075 (IN-FOLD). BEFORE 0.951–0.994 vs IN-FOLD 0.495–0.597.
- IN-FOLD vs NONE (descriptive, Table `tab:none_infold`): on T-12, correct oversampling helps M1 (+0.30), M5 (+0.17 to +0.18) and M3 (+0.11 to +0.12), barely changes M2 (+0.03) and **lowers** M4 (−0.04). So the honest T-12 range is NONE 0.292–0.563 vs IN-FOLD 0.495–0.597; the large gap to BEFORE (0.951–0.994) is not explained by oversampling being useful. On T-bin, IN-FOLD vs NONE changes almost nothing (−0.001 to +0.004).
- Explanation (mechanism, by construction): in BEFORE, test folds contain exact copies (OS-R) or SMOTE neighbours (OS-S) of training rows; the rare classes of T-12 are copied many times, so the classifier is largely tested on what it has seen. BEFORE test folds are not the IN-FOLD test rows, which is why RQ2 is descriptive (A-009); say so in Method/Threats.
- **Key message:** the BEFORE practice can turn a ~0.5–0.6 macro-F1 problem into an apparent ~0.95–0.99 result, comparable to the 98–99% figures reported in some studies.

### RQ3 (Table `tab:rq3`, primary protocol G-dup)
- M5 and M6 are clearly better **only than M3 (Random Forest)**: M5 vs M3 +0.032, M6 vs M3 +0.042 (Holm p ≤ 0.003).
- **No clear difference against M1, M2, M4** (6/8 comparisons). Under S the same 2/8 pattern holds (M5 vs M3 +0.030, M6 vs M3 +0.040).
- Interpretation: ensembles of correlated linear models (M1, M2) do not beat the best single linear model; the claimed ensemble gains in the literature are not supported here. As expected in the protocol, M5 behaves close to the better linear model.

### Replication on Dalpiaz (Table `tab:dalpiaz`, T-bin, M1–M5)
- BEFORE − IN-FOLD = +0.034 to +0.081, same direction as PROMISE_exp T-bin, comparable to fold SD (0.039–0.066) (descriptive). BEFORE 0.775–0.822 vs IN-FOLD 0.716–0.754.
- S vs LODO (unseen dataset): drop of **0.21–0.31** (S 0.709–0.746, LODO 0.405–0.511); descriptive only (n = 4 LODO folds). Kendall τ = 0.20.
- No-both sensitivity (appendix `tab:noboth`, descriptive): removing both-labelled rows raises M2–M5 by +0.035 to +0.074 and lowers M1 by 0.103.

### Overall
- Clear-difference counts (tested families only): RQ3-Gdup 2/8, RQ3-S 2/8. All other families are descriptive (Figure `fig:summary`).
- The re-run on 2026-10-18 reproduced every per-fold score bit-for-bit (SHA-256 of all fold-score files identical).

## 7. Error analysis (pending)

Sample: T-bin, G-dup, seed 42; 30 misclassified rows (15 M2 + 15 M5, each 8 true-NFR + 7 true-FR). Categories: mixed FR/NFR; quality keyword in FR; functional verb in NFR; ambiguous/underspecified; short/low context; possible annotation issue; other. Counts: **TODO after labelling** — do not invent them.

## 8. Recommendations to state in the paper

1. Oversample (and fit any vectorizer) inside the training fold only; never before splitting.
2. Report how duplicates were handled and group them when splitting; report the number of duplicate groups.
3. Report a project-level (or dataset-level) evaluation alongside random CV when claiming generalization.
4. Report macro-F1 per fold with repeated CV and a corrected paired test with multiple-comparison control before claiming that one model (e.g. an ensemble) is better.
5. Publish code, splits and per-fold scores.

## 9. Threats (to discuss)

Single main benchmark (+ one small replication); binary label hides mixed requirements; PROMISE label-quality concerns (`dalpiaz2019`); near-duplicate threshold 0.90 and one-person review of 14 candidate pairs; dependence between CV folds (the corrected t-test mitigates but does not remove it); uneven grouped folds (172–245 rows); fixed hyperparameters (no tuning, by design); BEFORE is a simplified reproduction of the practice, not each paper's exact pipeline; BEFORE test folds differ from IN-FOLD test folds (hence descriptive RQ2, A-009); classical models only (no transformers/LLMs); literature review limited to automatically downloadable open-access papers; error analysis on 30 rows only.

## 10. Citation keys (only these exist in `references.bib`)

- Datasets: `lima2019`, `clelandhuang2007`, `dalpiaz2019`, `dalpiaz2019data`
- Classic FR/NFR classification: `kurtanovic2017`, `abad2017what`, `clelandhuang2007`, `hey2020norbert`, `dalpiaz2019`
- Leakage / duplication: `kaufman2012`, `kapoor2023`, `allamanis2019adverse`
- Methods / tools: `chawla2002`, `nadeau2003`, `bouckaert2004`, `holm1979`, `pedregosa2011`, `lemaitre2017`
- Reviewed studies (21 counted): `khayashi2026deep`, `hey2020norbert`, `rahimi2020ensemble`, `alhoshan2023zero`, `rahimi2021phase`, `binkhonain2025prompts`, `or2025improving`, `abad2017what`, `abbas2024classification`, `tahir2025cross`, `metu2024hybrid`, `martin2025evaluating`, `kiani2026deep`, `kadhim2026enhancing`, `rahman2023functional`, `ali2025multi`, `eltahier2025bert`, `younas2019automated`, `li2025study`, `toth2019comparative`, `baskoro2021systematic`
- In the bib but excluded from the 21 (cite only if needed): `khurshid2022classification`, `li2019empirical`, `yahya2023novel`, `muhamad2023class`, `limaylla-lunarejo2023towards`, `khalid2026hybrid`, `talele2023semi`, `idate2024performance`
