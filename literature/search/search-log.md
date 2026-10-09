# Search Log – phat-tai

## 2026-10-09 · Stream Q1 – Core FR/NFR classification

`2026-10-09T06:36:48.137Z` → `2026-10-09T06:37:01.970Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("functional requirements" OR "non-functional requirements" OR "nonfunctional requirements" OR "quality requirements") AND (classification OR classifying OR classifier)
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | Q1 | `title_and_abstract.search: ("functional requirements" OR "non-functional requirements" OR "nonfunctional requirements" OR "quality requirements") AND (classification OR classifying OR classifier)` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 1300 | 200 | — |
| Semantic Scholar | Q1 | `("functional requirements" \| "non-functional requirements" \| "nonfunctional requirements" \| "quality requirements") + (classification \| classifying \| classifier)` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 911 | 200 | Chạy không có API key |
| arXiv | Q1 | `((all:"functional requirements" OR all:"non-functional requirements" OR all:"nonfunctional requirements" OR all:"quality requirements") AND (all:classification OR all:classifying OR all:classifier)) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 81 | 81 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 200/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 200/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 200/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 481 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **481** |
| ↳ DUPLICATE: trùng DOI | 43 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 24 |
| ↳ UNIQUE mới | 414 (trong đó 1 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 481 / 414 |

`query_match` của bản ghi UNIQUE mới: yes 311 · no 56 · unknown 47 (unknown = thiếu abstract).

---

## 2026-10-09 · Stream Q1b – Requirements classification + ML

`2026-10-09T06:37:01.994Z` → `2026-10-09T06:37:15.659Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("requirements classification" OR "requirement classification" OR "classifying requirements" OR "classification of requirements") AND ("machine learning" OR "deep learning" OR classifier OR classifiers OR "natural language processing" OR NLP)
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | Q1b | `title_and_abstract.search: ("requirements classification" OR "requirement classification" OR "classifying requirements" OR "classification of requirements") AND ("machine learning" OR "deep learning" OR classifier OR classifiers OR "natural language processing" OR NLP)` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 429 | 200 | — |
| Semantic Scholar | Q1b | `("requirements classification" \| "requirement classification" \| "classifying requirements" \| "classification of requirements") + ("machine learning" \| "deep learning" \| classifier \| classifiers \| "natural language processing" \| NLP)` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 304 | 200 | Chạy không có API key |
| arXiv | Q1b | `((all:"requirements classification" OR all:"requirement classification" OR all:"classifying requirements" OR all:"classification of requirements") AND (all:"machine learning" OR all:"deep learning" OR all:classifier OR all:classifiers OR all:"natural language processing" OR all:NLP)) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 187 | 187 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 200/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 200/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 200/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 587 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **587** |
| ↳ DUPLICATE: trùng DOI | 149 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 27 |
| ↳ UNIQUE mới | 411 (trong đó 2 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 1068 / 825 |

`query_match` của bản ghi UNIQUE mới: yes 149 · no 228 · unknown 34 (unknown = thiếu abstract).

---

## 2026-10-09 · Stream Q2 – Ensemble

`2026-10-09T06:37:15.687Z` → `2026-10-09T06:37:23.693Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("requirements classification" OR "requirement classification" OR "classifying requirements") AND (ensemble OR voting OR stacking OR bagging OR boosting)
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | Q2 | `title_and_abstract.search: ("requirements classification" OR "requirement classification" OR "classifying requirements") AND (ensemble OR voting OR stacking OR bagging OR boosting)` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 55 | 55 | — |
| Semantic Scholar | Q2 | `("requirements classification" \| "requirement classification" \| "classifying requirements") + (ensemble \| voting \| stacking \| bagging \| boosting)` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 38 | 38 | Chạy không có API key |
| arXiv | Q2 | `((all:"requirements classification" OR all:"requirement classification" OR all:"classifying requirements") AND (all:ensemble OR all:voting OR all:stacking OR all:bagging OR all:boosting)) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 5 | 5 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 200/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 200/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 200/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 98 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **98** |
| ↳ DUPLICATE: trùng DOI | 72 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 10 |
| ↳ UNIQUE mới | 16 (trong đó 0 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 1166 / 841 |

`query_match` của bản ghi UNIQUE mới: yes 7 · no 7 · unknown 2 (unknown = thiếu abstract).

---

## 2026-10-09 · Stream Q3 – PROMISE dataset

`2026-10-09T06:37:23.729Z` → `2026-10-09T06:37:31.385Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("PROMISE_exp" OR "PROMISE NFR" OR "PROMISE dataset" OR "PROMISE repository" OR "PROMISE corpus") AND requirements
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | Q3 | `title_and_abstract.search: ("PROMISE_exp" OR "PROMISE NFR" OR "PROMISE dataset" OR "PROMISE repository" OR "PROMISE corpus") AND requirements` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 110 | 110 | — |
| Semantic Scholar | Q3 | `("PROMISE_exp" \| "PROMISE NFR" \| "PROMISE dataset" \| "PROMISE repository" \| "PROMISE corpus") + requirements` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 76 | 76 | Chạy không có API key |
| arXiv | Q3 | `((all:"PROMISE_exp" OR all:"PROMISE NFR" OR all:"PROMISE dataset" OR all:"PROMISE repository" OR all:"PROMISE corpus") AND all:requirements) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 5 | 5 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 200/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 200/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 200/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 191 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **191** |
| ↳ DUPLICATE: trùng DOI | 126 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 13 |
| ↳ UNIQUE mới | 52 (trong đó 0 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 1357 / 893 |

`query_match` của bản ghi UNIQUE mới: yes 37 · no 2 · unknown 13 (unknown = thiếu abstract).

---

## 2026-10-09 · Stream Q4 – Generalization / evaluation / leakage

`2026-10-09T06:37:31.421Z` → `2026-10-09T06:37:49.912Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("requirements classification" OR "requirement classification") AND ("cross-project" OR "cross-domain" OR generalization OR generalisation OR leakage OR duplicate OR "cross-validation")
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | Q4 | `title_and_abstract.search: ("requirements classification" OR "requirement classification") AND ("cross-project" OR "cross-domain" OR generalization OR generalisation OR leakage OR duplicate OR "cross-validation")` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 32 | 32 | — |
| Semantic Scholar | Q4 | `("requirements classification" \| "requirement classification") + ("cross-project" \| "cross-domain" \| generalization \| generalisation \| leakage \| duplicate \| "cross-validation")` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 23 | 23 | Chạy không có API key |
| arXiv | Q4 | `((all:"requirements classification" OR all:"requirement classification") AND (all:"cross-project" OR all:"cross-domain" OR all:generalization OR all:generalisation OR all:leakage OR all:duplicate OR all:"cross-validation")) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 21 | 21 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 200/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 200/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 200/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 76 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **76** |
| ↳ DUPLICATE: trùng DOI | 47 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 15 |
| ↳ UNIQUE mới | 14 (trong đó 0 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 1433 / 907 |

`query_match` của bản ghi UNIQUE mới: yes 4 · no 7 · unknown 3 (unknown = thiếu abstract).

---

## 2026-10-09 · Stream Q5 – Preprocessing

`2026-10-09T06:38:32.309Z` → `2026-10-09T06:38:35.858Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("requirements classification" OR "requirement classification") AND (preprocessing OR "stop words" OR stopwords OR lemmatization OR stemming OR "TF-IDF")
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | Q5 | `title_and_abstract.search: ("requirements classification" OR "requirement classification") AND (preprocessing OR "stop words" OR stopwords OR lemmatization OR stemming OR "TF-IDF")` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 52 | 52 | — |
| Semantic Scholar | Q5 | `("requirements classification" \| "requirement classification") + (preprocessing \| "stop words" \| stopwords \| lemmatization \| stemming \| "TF-IDF")` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 37 | 37 | Chạy không có API key |
| arXiv | Q5 | `((all:"requirements classification" OR all:"requirement classification") AND (all:preprocessing OR all:"stop words" OR all:stopwords OR all:lemmatization OR all:stemming OR all:"TF-IDF")) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 3 | 3 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 500/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 500/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 500/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 92 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **92** |
| ↳ DUPLICATE: trùng DOI | 83 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 8 |
| ↳ UNIQUE mới | 1 (trong đó 0 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 1525 / 908 |

`query_match` của bản ghi UNIQUE mới: yes 1 · no 0 · unknown 0 (unknown = thiếu abstract).

---

## 2026-10-09 · Stream T1 – Data leakage trong ML (nền tảng)

`2026-10-09T06:38:35.898Z` → `2026-10-09T06:38:47.721Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("data leakage" OR "near-duplicate" OR "duplicate data" OR "code duplication") AND ("machine learning") AND (evaluation OR reproducibility OR "performance estimates")
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | T1 | `title_and_abstract.search: ("data leakage" OR "near-duplicate" OR "duplicate data" OR "code duplication") AND "machine learning" AND (evaluation OR reproducibility OR "performance estimates")` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 1389 | 100 | — |
| Semantic Scholar | T1 | `("data leakage" \| "near-duplicate" \| "duplicate data" \| "code duplication") + "machine learning" + (evaluation \| reproducibility \| "performance estimates")` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 860 | 100 | Chạy không có API key |
| arXiv | T1 | `((all:"data leakage" OR all:"near-duplicate" OR all:"duplicate data" OR all:"code duplication") AND all:"machine learning" AND (all:evaluation OR all:reproducibility OR all:"performance estimates")) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 239 | 100 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 100/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 100/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 100/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 300 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **300** |
| ↳ DUPLICATE: trùng DOI | 13 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 26 |
| ↳ UNIQUE mới | 261 (trong đó 2 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 1825 / 1169 |

`query_match` của bản ghi UNIQUE mới: yes 136 · no 107 · unknown 18 (unknown = thiếu abstract).

---

## 2026-10-09 · Stream T2 – So sánh classifier bằng thống kê (nền tảng)

`2026-10-09T06:38:47.766Z` → `2026-10-09T06:39:06.221Z` · slr-metadata-fetcher v3.0.0-frnfr · protocol research_protocol.md v1.1 (2026-10-09) · thành viên: phat-tai

Chuỗi chuẩn (canonical query):

```text
("corrected resampled t-test" OR "repeated cross-validation" OR "comparing classifiers" OR "comparing learning algorithms") AND (significance OR "statistical test" OR "t-test")
```

| database | search_stream | exact_query_used | search_fields | filters | date | result_count | exported_count | notes |
|---|---|---|---|---|---|---:|---:|---|
| OpenAlex | T2 | `title_and_abstract.search: ("corrected resampled t-test" OR "repeated cross-validation" OR "comparing classifiers" OR "comparing learning algorithms") AND (significance OR "statistical test" OR "t-test")` | title + abstract (title_and_abstract.search) | publication_year:>2016; publication_year:<2027; năm 2017–2026 | 2026-10-09 | 110 | 100 | — |
| Semantic Scholar | T2 | `("corrected resampled t-test" \| "repeated cross-validation" \| "comparing classifiers" \| "comparing learning algorithms") + (significance \| "statistical test" \| "t-test")` | title + abstract (paper/search/bulk) | year=2017-2026; năm 2017–2026 | 2026-10-09 | 70 | 70 | Chạy không có API key |
| arXiv | T2 | `((all:"corrected resampled t-test" OR all:"repeated cross-validation" OR all:"comparing classifiers" OR all:"comparing learning algorithms") AND (all:significance OR all:"statistical test" OR all:"t-test")) AND submittedDate:[201701010000 TO 202612312359]` | all fields (all:) | năm 2017–2026 | 2026-10-09 | 10 | 10 | — |

- **OpenAlex:** endpoint `https://api.openalex.org/works` · sort: mặc định (relevance), phân trang cursor · limit: 100/nguồn
- **Semantic Scholar:** endpoint `https://api.semanticscholar.org/graph/v1/paper/search/bulk` · sort: mặc định của bulk search, phân trang token · limit: 100/nguồn
- **arXiv:** endpoint `https://export.arxiv.org/api/query` · sort: relevance desc · limit: 100/nguồn

| Bước | Số lượng |
|---|---:|
| Bản ghi thu về (exported) | 180 |
| Bỏ do ngoài khung năm | 0 |
| Bỏ do lạc đề ở nguồn không boolean (Crossref/CORE, không ghi vào 01) | 0 |
| Đã có từ lần chạy trước (cùng nguồn + stream, không ghi lại) | 0 |
| **Ghi vào 01_all_records.csv** | **180** |
| ↳ DUPLICATE: trùng DOI | 56 |
| ↳ DUPLICATE: trùng tiêu đề + tác giả + năm | 17 |
| ↳ UNIQUE mới | 107 (trong đó 0 có cờ POSSIBLE-DUP) |
| Tổng dòng trong 01 / số bản ghi UNIQUE | 2005 / 1276 |

`query_match` của bản ghi UNIQUE mới: yes 66 · no 28 · unknown 13 (unknown = thiếu abstract).
