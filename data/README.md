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

## Cách lấy lại raw data (nếu không chia sẻ được file)

1. Tải từ `canonical_url` ở trên.
2. Lưu vào `data/raw/` với đúng tên file, không mở bằng Excel rồi lưu lại.
3. Kiểm tra: `Get-FileHash .\data\raw\<file> -Algorithm SHA256` phải khớp `checksums.csv`.

## Processed

`data/processed/requirements.csv`: `requirement_id, text, label, project_id, duplicate_group`, sinh bằng `src/audit_dataset.py` từ raw. Không chỉnh tay.

`data/processed/near_duplicate_review.csv`: `group_a, group_b, cosine, text_a, text_b, decision_A, decision_B, final, note`, quyết định tay cho cặp near-duplicate (protocol §4.2).
