# Research Protocol v1

## Title

A Reproducible and Leakage-Aware Evaluation of Ensemble Learning
for Functional and Non-Functional Software Requirements Classification

## Task

Binary classification:

- Functional
- Non-Functional

## Research Questions

RQ1:
How do individual machine-learning classifiers and ensemble
methods compare in binary FR/NFR classification?

RQ2:
How do common NLP preprocessing strategies affect
FR/NFR classification performance?

RQ3:
Do model performance and ensemble improvements remain
consistent under leakage-aware evaluation?

## Dataset

PROMISE / PROMISE_exp

## Representation

TF-IDF

## Models

M1 Logistic Regression
M2 Linear SVM
M3 Random Forest
M4 Hard Voting
M5 Stacking

## Preprocessing

P0 Minimal
P1 Stopword removal
P2 Stopword removal + lemmatization

## Feature configurations

F1 unigram
F2 unigram + bigram

## Evaluation

A. Repeated Stratified 5-Fold CV
B. Leakage-aware Stratified Group CV

## Primary Metric

Macro-F1

## Secondary Metrics

Accuracy
Precision
Recall
F1-FR
F1-NFR

## Seeds

42
123
2026
3407
9917
