# FR/NFR Ensemble — Leakage-Aware Evaluation

A Reproducible and Leakage-Aware Evaluation of Ensemble Learning for Functional and Non-Functional Software Requirements Classification. Nhóm 2 người, 4 tuần (09/10 → 05/11/2026).

- Protocol (nguồn chuẩn cho mọi quyết định thí nghiệm): [protocol/research_protocol.md](protocol/research_protocol.md)
- Thay đổi sau khi khóa protocol: [protocol/amendment_log.md](protocol/amendment_log.md)
- Nhật ký hằng ngày: [research_log.md](research_log.md) · Nhật ký chạy: [experiments/experiment_log.csv](experiments/experiment_log.csv)

| Vai trò | Phụ trách |
|---|---|
| Hoang Anh (TV A) | protocol, dataset, audit, preprocessing, splits |
| Phat Tai (TV B) | literature, models, thống kê, bảng/hình |
| Cả hai | review code split/leakage, xác nhận số liệu, Discussion |

## Môi trường

Python 3.12 **win-amd64** (không dùng MinGW/MSYS2).

```powershell
python -c "import sysconfig; print(sysconfig.get_platform())"   # phải là win-amd64
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -c "import nltk; [nltk.download(r) for r in ('stopwords','wordnet','omw-1.4','averaged_perceptron_tagger_eng')]"
```

Khi thêm package: `python -m pip freeze | Set-Content -Encoding ascii requirements.txt` (không dùng `>` trong Windows PowerShell 5.1 vì sẽ ra UTF-16).

## Lệnh

```powershell
# Literature (công cụ chính, chạy từ thư mục cha NCKH/, kết quả vào literature/search/):
#   node tools/frnfr-metadata-fetcher/cli.mjs fetch --member phat-tai --streams core --max 200
#   node tools/frnfr-metadata-fetcher/cli.mjs screen --member phat-tai
# Dự phòng chỉ OpenAlex (key tùy chọn: $env:OPENALEX_API_KEY = "...")
python scripts/harvest_openalex.py --max 100

# Dataset: freeze file thô (điền metadata đã xác minh, chưa rõ thì UNKNOWN)
python scripts/freeze_dataset.py data/raw/<file> --name PROMISE_exp --url "<url>" --license UNKNOWN --retrieved 2026-10-10 --expected-rows 969

# Thí nghiệm (sẽ có từ tuần 2)
python experiments/run_smoke.py
python experiments/run_all.py
```

## Cấu trúc

```text
protocol/      research_protocol.md, amendment_log.md
literature/    search/ (output của frnfr-metadata-fetcher), 01_openalex_screening.csv (dự phòng), openalex_search_manifest.json, search-log.md, literature_matrix.xlsx (snapshot; bản chính là Google Sheet trên Drive nhóm), references.bib
data/          README.md, raw/ (không push), processed/, dataset_manifest.json, checksums.csv
scripts/       harvest_openalex.py, freeze_dataset.py
src/           audit_dataset.py, preprocessing.py, features.py, models.py, splits.py, stacking.py, evaluation.py, stats.py
experiments/   run_smoke.py, run_all.py, experiment_log.csv
tests/         test_splits.py, test_leakage.py, test_preprocessing.py
results/       tables/, figures/, predictions/ (không push)
manuscript/    paper (template LNCS hoặc theo môn), figures/
```
