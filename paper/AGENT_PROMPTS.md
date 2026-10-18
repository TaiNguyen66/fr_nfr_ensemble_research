# Prompts for writing the paper with ChatGPT / Gemini

Workflow per section:

1. Open a **new chat**.
2. Paste **Block 0 (rules)**, then the full text of `fact_sheet.md`, then the section prompt below.
3. Paste the agent's LaTeX into `sections/<file>.tex` on Overleaf. Replace only the `TODO` lines and keep the `\input{...}` / figure commands.
4. Recompile and check that there are no `[?]` citations or `??` references.
5. Send the draft back to the checking session (Claude) with **Block R** for a fact check before it counts as done.

Recommended order: Method → Results → Discussion → Threats → Related Work → Introduction → Conclusion → Abstract.

---

## Block 0: rules (paste first, every time)

```
You are helping write a two-column IEEE-style research paper in LaTeX (IEEEtran, pdfLaTeX, BibTeX).
Title: "How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification? A Leakage-Aware
Re-Evaluation of Single and Ensemble Classifiers".

Hard rules:
1. Use ONLY facts and numbers from the FACT SHEET I give you. Never invent, round differently, or
   "improve" a number. Use 3 decimals for macro-F1 values and differences, as in the fact sheet.
2. Cite ONLY with \cite{key} using keys listed in the FACT SHEET section 10. Never add a reference,
   never invent a key, author, year or DOI. If a claim needs a source that is not listed, write
   % TODO-CITE and leave it to me.
3. Wording rules: say "clear difference" only where the fact sheet says so; otherwise "no clear
   difference". Do not call RQ1(a) or RQ1(b) "leakage". Do not claim our models beat published results.
   Report negative results plainly.
4. Do not create or edit tables or figures; refer to them with \ref{tab:rq1}, \ref{tab:rq2},
   \ref{tab:rq3}, \ref{tab:dalpiaz}, \ref{tab:none_infold}, \ref{tab:kendall}, \ref{tab:noboth},
   \ref{fig:design}, \ref{fig:summary}.
5. Output only LaTeX for the section body (no \documentclass, no preamble). Escape _ as \_ and % as \%.
   Use "macro-F1", "PROMISE\_exp", "FR/NFR".
6. Style: academic, concise, past tense for what we did, present tense for what results show.
   No hype words ("groundbreaking", "remarkable", "significantly" unless statistically meant).
7. Mark anything you are unsure about with % CHECK: <reason>.
```

---

## Section prompts

### Method → `sections/method.tex` (~1.5 pages)

```
Write the "Study Design" section body (the \section line, figure fig:design and the TODO are already in
the file; give me the text that replaces the TODO). Subsections:
\subsection{Datasets and tasks} (PROMISE_exp, duplicate groups, T-bin/T-12, Dalpiaz replication incl.
label mapping and no-both sensitivity),
\subsection{Pipeline and models} (P0 preprocessing, TF-IDF fitted in-fold, M0-M6, stacking inner CV),
\subsection{Evaluation protocols} (S, G-dup, G-proj, LODO; 5 seeds x 5 folds; refer to Fig.~\ref{fig:design}),
\subsection{Oversampling conditions} (NONE, IN-FOLD, BEFORE; OS-R/OS-S; explain that BEFORE test folds
contain copies/synthetic neighbours of training rows and are paired with IN-FOLD folds by (seed, fold) index),
\subsection{Metrics and statistical analysis} (macro-F1 per fold, corrected repeated k-fold t-test, Holm per
family, the |Delta| >= 0.01 rule, families and their sizes, descriptive-only parts),
\subsection{Reproducibility} (protocol locked before any run, run counts, bit-identical re-run, public code).
Cite pedregosa2011, lemaitre2017, chawla2002, nadeau2003, bouckaert2004, holm1979, lima2019, dalpiaz2019,
dalpiaz2019data where appropriate.
```

### Results → `sections/results.tex` (~1.5–2 pages)

```
Write the text for each Results subsection (replace each TODO; the \input{tables/...} lines stay).
Start with 2-3 sentences before the first subsection that point to Fig.~\ref{fig:summary} and summarise
the clear-difference counts. Then RQ1 (a then b, incl. Kendall tau and fold SD), RQ2 (T-bin then T-12,
then NONE vs IN-FOLD from Table~\ref{tab:none_infold}), RQ3, Replication (incl. S vs LODO descriptive
and the no-both appendix Table~\ref{tab:noboth}). Leave "Error analysis" as TODO.
Only describe results; interpretation goes to Discussion. Each subsection ends with one bold
"Answer to RQx:" sentence.
```

### Discussion → `sections/discussion.tex` (~0.8 page)

```
Write the Discussion. Paragraphs: (1) Why oversampling before splitting inflates T-12 so much and T-bin
little (mechanism in fact sheet; link to the 98-99% figures reported by metu2024hybrid and
baskoro2021systematic WITHOUT saying those papers are wrong). (2) Duplicates: negative finding on this
dataset, why (8 groups), when it could matter (larger or scraped corpora; allamanis2019adverse).
(3) Project-level drop and ranking change: what random CV estimates vs what practitioners need
(not leakage). (4) Ensembles: no gain over the best linear model; why (correlated base models); link to
untested ensemble claims (G3). (5) Recommendations: the 5 items of fact sheet section 8 as a short list.
```

### Threats → `sections/threats.tex` (~0.5 page)

```
Write "Threats to Validity" with four paragraphs: Construct, Internal, External, Conclusion validity.
Use only the items in fact sheet section 9, and say for each what we did to mitigate it.
```

### Related Work → `sections/related_work.tex` (~0.8 page)

```
Write Related Work in three subsections: \subsection{FR/NFR requirements classification}
(clelandhuang2007, kurtanovic2017, abad2017what, hey2020norbert, dalpiaz2019, then recent ML/DL/LLM work
from the reviewed-studies keys, grouped by approach, 1 sentence per group, several keys per \cite);
\subsection{Evaluation pitfalls: leakage and duplication} (kaufman2012, kapoor2023, allamanis2019adverse);
\subsection{Evaluation practice in FR/NFR studies} (our review of 21 studies: G1-G6 counts with the
example keys from fact sheet section 2; end with the gap this paper fills).
```

### Introduction → `sections/introduction.tex` (~1 page)

```
Write the Introduction: context (why FR/NFR classification matters, PROMISE benchmarks), problem (very
high reported scores; evaluation choices like random splits, oversampling before split, untested
ensemble claims), evidence from our review (counts), what we do (leakage-aware re-evaluation, fixed
protocol locked in advance), the three RQs as an enumerated list, main findings in 3 bullets
(numbers from the fact sheet), contributions as an itemized list (measurement of inflation, protocol and
recommendations, reproducible package), and a one-sentence paper outline using \ref{sec:...}
(sec:related, sec:method, sec:results, sec:discussion, sec:threats, sec:conclusion).
```

### Conclusion → `sections/conclusion.tex` (~0.3 page)

```
Write the Conclusion (replace the TODO; keep the Data and Code Availability section). One paragraph of
findings, one of take-aways for researchers, one of future work (transformers/LLMs under the same
protocol, other datasets with more duplicates, error-analysis-driven label review).
```

### Abstract → `sections/abstract.tex` (150–200 words)

```
Write the abstract (replace TODO only): context, problem, method (datasets, models, protocols,
corrected tests), key numbers (G-proj drop 0.13-0.19; BEFORE inflation +0.39 to +0.49 on 12 classes,
not clear on binary; no duplicate effect; ensembles only beat RF), and the main recommendation.
No citations in the abstract.
```

---

## Block R: review request (paste into the checking session with the draft)

```
Check this draft of <section> against fact_sheet.md and the tables in paper/tables. List every number,
citation key or wording that does not match (protocol §10 rules), with the exact fix.
```
