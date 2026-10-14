# Data

Điền sau khi xác minh nguồn (checklist D1). Trường chưa xác minh ghi `UNKNOWN`, không đoán.

## Dataset chính

| Trường | Giá trị |
|---|---|
| dataset_name | PROMISE_exp |
| canonical_url | Bản mirror: https://github.com/AleksandarMitrevski/se-requirements-classification/tree/master/0-datasets/PROMISE_exp (chưa tìm thấy bản phát hành gốc của tác giả) |
| doi | 10.1145/3350768.3350776 (bài gốc) |
| source_paper | Lima, M., Valle, V., Costa, E., Lira, F., Gadelha, B. (2019). Software Engineering Repositories: Expanding the PROMISE Database. SBES 2019 |
| version / commit | mirror nhánh master, tải 2026-10-14 |
| license | UNKNOWN |
| retrieved_date | 2026-10-14 |
| raw file | `data/raw/PROMISE_exp.arff` (115.622 byte, ARFF: ProjectID, RequirementText, class) |
| SHA-256 | xem `checksums.csv` |
| expected (Promise+, SBES 2024) | 969 dòng, 444 FR / 525 NFR, cột `ProjectID`, `RequirementText`, `Class` |
| actual (audit nhanh 14/10) | 969 dòng; 444 FR / 525 NFR; 12 mã lớp (F 444, SE 125, US 85, O 77, PE 67, LF 49, A 31, MN 24, SC 22, FT 18, L 15, PO 12); 47 project (1–92 dòng/project); 3 nhóm câu trùng chính xác (6 dòng, không xung đột nhãn, 2 nhóm khác project); 14 cặp gần trùng cosine ≥ 0,90 cần duyệt tay; G-proj đạt quy tắc khả thi với 5 fold |
| discrepancy | Không có so với mô tả trong bài gốc |

## Dataset phụ (kiểm tra lại, A-007): Dalpiaz et al. 2019

| Trường | Giá trị |
|---|---|
| dataset_name | Dalpiaz2019: dronology, leeds, reqview, wasp |
| canonical_url | https://zenodo.org/records/3309582 (`RE2019-Paper96.zip`, thư mục `Manually tagged datasets/`) |
| doi | 10.5281/zenodo.3309582 |
| source_paper | Dalpiaz, F., Dell'Anna, D., Aydemir, F. B., Çevikol, S. (2019). Requirements Classification with Interpretable Machine Learning and Dependency Parsing. RE 2019 |
| version | Zenodo v1 (2019-07-10); SHA-256 của zip `8e274e26…36f6` |
| license | GPL-3.0 (`data/raw/dalpiaz2019/LICENSE.md`) |
| retrieved_date | 2026-10-14 |
| raw files | `data/raw/dalpiaz2019/{dronology,leeds,reqview,wasp}.csv`; cột `ProjectID, RequirementText, IsFunctional, IsQuality` (đa nhãn) |
| loại khỏi gói | `promise-reclass` (trùng nguồn với PROMISE_exp); `ds2`, `ds3`, `esa-eucl-est` (cột text để trống, dữ liệu riêng); các file `*combined` (gộp) |
| audit (14/10) | 331 dòng: dronology 97, leeds 85, reqview 87, wasp 62. 0 câu trùng trong bộ, 0 câu trùng với PROMISE_exp. Nhãn: F-only 187, Q-only 59, cả hai 81, không nhãn 4 |
| quy về FR/NFR (chốt trước khi chạy) | IsQuality = 1 → NFR (kể cả câu có cả hai nhãn); chỉ IsFunctional = 1 → FR; không nhãn → loại. Kết quả: **327 dòng, 187 FR / 140 NFR** (dronology 68/28, leeds 23/61, reqview 54/32, wasp 42/19). Kiểm tra độ nhạy: bỏ 81 câu có cả hai nhãn |
| khả thi leave-one-dataset-out | 4 fold, mỗi fold 61–96 dòng, tỉ lệ lớp nhỏ thấp nhất 0,27 (leeds) → đạt quy tắc G-proj (≥ 2 nhóm trong train, ≥ 10 % dòng, lớp nhỏ ≥ 0,20) |
| hạn chế | Nhỏ (327 dòng), chỉ 4 project; mất cân bằng nhẹ (57/43) nên hiệu ứng oversampling có thể nhỏ hơn PROMISE_exp; nhãn đa nhãn phải quy đổi |

## Cách lấy lại raw data (nếu không chia sẻ được file)

1. Tải từ `canonical_url` ở trên.
2. Lưu vào `data/raw/` với đúng tên file, không mở bằng Excel rồi lưu lại.
3. Kiểm tra: `Get-FileHash .\data\raw\<file> -Algorithm SHA256` phải khớp `checksums.csv`.

## Processed

`data/processed/requirements.csv`: `requirement_id, text, label, project_id, duplicate_group`, sinh bằng `src/audit_dataset.py` từ raw. Không chỉnh tay.

`data/processed/near_duplicate_review.csv`: `group_a, group_b, cosine, text_a, text_b, decision_A, decision_B, final, note`, quyết định tay cho cặp near-duplicate (protocol §4.2).
