# FR/NFR Ensemble — Leakage-Aware Evaluation

Working title: *A Reproducible and Leakage-Aware Evaluation of Ensemble Learning for Functional and Non-Functional Software Requirements Classification* (chốt sau giai đoạn 3). Nhóm 2 người, 09/10 → 05/11/2026.

Quy trình 4 giai đoạn: **(1)** chọn chủ đề & kiểm tra tài liệu → **(2)** chọn & tổng hợp tài liệu → **(3)** đọc, so sánh & tìm khoảng trống → **(4)** triển khai end-to-end.

- Review tài liệu (GĐ1–3, tiêu chí từng vòng sàng lọc): [protocol/review_protocol.md](protocol/review_protocol.md)
- Thiết kế thí nghiệm (GĐ4; v1.1 là thiết kế ứng viên, chốt v2.0 ngày 22/10): [protocol/research_protocol.md](protocol/research_protocol.md)
- Thay đổi sau khi khóa protocol: [protocol/amendment_log.md](protocol/amendment_log.md)
- Nhật ký hằng ngày: [research_log.md](research_log.md) · Nhật ký chạy: [experiments/experiment_log.csv](experiments/experiment_log.csv)

| Vai trò | Phụ trách |
|---|---|
| Hoang Anh (TV A) | sàng lọc ~40%; mạch dữ liệu song song (nguồn, freeze, audit); preprocessing, splits |
| Phat Tai (TV B) | chủ trì review tài liệu (~60% sàng lọc), tổng hợp & gap; models, thống kê, bảng/hình |
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
# Workbook sàng lọc R1–R3 + bảng gap (đưa lên Drive, lưu dưới dạng Google Sheet):
python scripts/build_screening_workbook.py
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
protocol/      review_protocol.md, research_protocol.md, amendment_log.md
literature/    search/ (output frnfr-metadata-fetcher), review/ (workbook sàng lọc + bản chụp sau mỗi vòng R1/R2/R3; bản làm việc là Google Sheet trên Drive), references.bib
data/          README.md, raw/ (không push), processed/, dataset_manifest.json, checksums.csv
scripts/       build_screening_workbook.py, freeze_dataset.py, harvest_openalex.py (dự phòng)
src/           audit_dataset.py, preprocessing.py, features.py, models.py, splits.py, stacking.py, evaluation.py, stats.py
experiments/   run_smoke.py, run_all.py, experiment_log.csv
tests/         test_splits.py, test_leakage.py, test_preprocessing.py
results/       tables/, figures/, predictions/ (không push)
manuscript/    paper (template LNCS hoặc theo môn), figures/
```
