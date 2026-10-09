# Data

Điền sau khi xác minh nguồn (checklist D1). Trường chưa xác minh ghi `UNKNOWN`, không đoán.

## Dataset chính

| Trường | Giá trị |
|---|---|
| dataset_name | PROMISE_exp |
| canonical_url | UNKNOWN |
| doi | UNKNOWN |
| source_paper | UNKNOWN (dự kiến: bài giới thiệu PROMISE_exp, cần xác minh) |
| version / commit | UNKNOWN |
| license | UNKNOWN |
| retrieved_date | UNKNOWN |
| raw file | `data/raw/<tên file thực tế>` |
| SHA-256 | xem `checksums.csv` |
| expected (Promise+, SBES 2024) | 969 dòng, 444 FR / 525 NFR, cột `ProjectID`, `RequirementText`, `Class` |
| actual (sau audit) | |
| discrepancy | |

## Cách lấy lại raw data (nếu không chia sẻ được file)

1. Tải từ `canonical_url` ở trên.
2. Lưu vào `data/raw/` với đúng tên file, không mở bằng Excel rồi lưu lại.
3. Kiểm tra: `Get-FileHash .\data\raw\<file> -Algorithm SHA256` phải khớp `checksums.csv`.

## Processed

`data/processed/requirements.csv`: `requirement_id, text, label, project_id, duplicate_group`, sinh bằng `src/audit_dataset.py` từ raw. Không chỉnh tay.

`data/processed/near_duplicate_review.csv`: `group_a, group_b, cosine, text_a, text_b, decision_A, decision_B, final, note`, quyết định tay cho cặp near-duplicate (protocol §4.2).
