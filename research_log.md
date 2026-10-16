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
