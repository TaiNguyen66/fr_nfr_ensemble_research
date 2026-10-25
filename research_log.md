# Research log

Mỗi ngày làm việc thêm một mục (mới nhất ở cuối). Ghi cả việc hỏng và quyết định nhỏ; số liệu chính để trong `results/`, ở đây chỉ dẫn link.

```text
## YYYY-MM-DD — <Hoang Anh | Phat Tai>
Done (link file/commit):
Blockers:
Decisions (amendment ID nếu đổi scope):
Next:
Needs review from:
```

---

## 2026-10-16 — Phat Tai
Done: protocol LOCKED (A-008, commit d2b08c6); `src/analyze_results.py` + 6 tests (34 pass); `audit_dataset` khớp handoff; chạy xong plan RQ1 (21 cấu hình, 525 fold, ~6.6 phút, `results/tables/fold_scores_RQ1.csv`, log `logs/run_RQ1.txt`, experiment_log 7789603a).
Blockers: không.
Decisions: A-008 (Phat Tai là người duy nhất phê duyệt; RQ1-D2 báo cáo mô tả, không kiểm định).
Next: chạy RQ2 và D2, rồi `python -m src.analyze_results`.
Needs review from: —

## 2026-10-16 (tiếp) — Phat Tai
Done: chạy xong RQ2 (50 cấu hình, 1250 fold, 611 s) và D2 (35 cấu hình, 770 fold, 150 s); RQ1 398 s. Chạy `python -m src.analyze_results` → `results/tables/stats_*.csv`, `summary_*.csv`, `descriptive_*.csv`, `kendall_tau.csv`, `results/figures/delta_*.png`.
Blockers: không.
Decisions: không đổi thiết kế; không chạy lại cấu hình nào.
Next: error analysis §11 (T-bin, G-dup, seed 42, M2 và M5); viết Results; kiểm chứng chạy lại sạch ngày 02/11.
Needs review from: —

## 2026-10-18 — Phat Tai
Done: kiểm chứng chạy lại sạch trên máy cá nhân: pytest 34 passed; audit_dataset khớp; chạy lại RQ1 (413 s), RQ2 (710 s), D2 (174 s), analyze_results. SHA-256 cả 3 `fold_scores_*.csv` trùng lần 2026-10-16, `git diff --stat results/tables` rỗng → tái lập đúng từng bit.
Blockers: không.
Decisions: `splits_D2.csv` chỉ đổi thứ tự khối (thứ tự duyệt `set` không cố định) → sửa `run_experiments.py` dùng `sorted(...)`, khôi phục file đã commit; không đổi thiết kế, không cần amendment. Không dùng Colab cho lần kiểm chứng này.
Next: push (sau khi Phat Tai đồng ý); bảng phụ lục no-both D2; gán nhãn error analysis; viết Results.
Needs review from: —

## 2026-10-25 — Phat Tai
Done: viết bản nháp đủ 8 section (commit 61fba32); bib thêm URL DOI, phụ lục trước References; Table 5 một cột; thông tin tác giả (3b1ac44, 49b476c, 3d34c4a); script ghép nhãn error analysis (aeb4071). Gán nhãn error analysis phía Phat Tai (có hỗ trợ AI, đã duyệt). Phê duyệt và triển khai A-009: RQ1-dup, RQ1-proj, RQ2-bin, RQ2-12, RQ2-D2 chỉ báo cáo mô tả; kiểm định chỉ còn cho RQ3; sửa analyze_results, paper_tables, test, bảng/hình, fact_sheet và các section.
Blockers: không.
Decisions: A-009 (đề xuất Hoang Anh, Phat Tai mở rộng sang RQ2). Không chạy lại model; Δ trung bình không đổi.
Next: Hoang Anh cập nhật mục Error analysis theo nhãn đã thống nhất (15/30, κ = 0.391; nhãn hai phía đều có hỗ trợ AI); soát bài; biên dịch IEEEtran.
Needs review from: Hoang Anh

## 2026-10-26 — Hoang Anh

Done: Hoàn thành Error Analysis theo protocol §11. Đối chiếu 30/30 nhãn của Hoàng Anh và Phát Tài với dữ liệu đã thực hiện trước đó; toàn bộ row_id và nhãn ban đầu khớp. Agreement trước hòa giải: 15/30 (50.0%), Cohen's kappa = 0.3911. Hoàn tất hòa giải 30/30 câu, kiểm tra thành công bằng `scripts/reconcile_error_labels.py counts`. Phân bố 7 nhóm lỗi: 8, 7, 6, 4, 2, 2, 1. Cập nhật `paper/sections/results.tex`, `paper/sections/threats.tex` và `paper/fact_sheet.md` trên phiên bản đã tích hợp A-009. Ghi rõ cả hai tác giả sử dụng AI hỗ trợ trong quá trình gán nhãn.

Blockers: Không có đối với phần Error Analysis. Cần Phát Tài kiểm tra nội dung paper và biên dịch IEEEtran trên Overleaf.

Decisions: Tái sử dụng kết quả gán nhãn và hòa giải cũ sau khi xác minh với file Phát Tài bàn giao. Không chạy lại mô hình, không thay đổi nhãn gốc. A-009 đã được Phát Tài phê duyệt và triển khai; giữ nguyên các thay đổi thống kê của A-009.

Next: Chạy pytest trên phiên bản mới, kiểm tra Git, commit và push nội dung Error Analysis; gửi Phát Tài commit hash, Agreement, Kappa và bảng đếm chính thức.

Needs review from: Phat Tai — Error Analysis, tính nhất quán của paper và bản biên dịch IEEEtran.