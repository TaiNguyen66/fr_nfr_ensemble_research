# Results — khung bài (Phat Tai)

Số liệu dưới đây là của lần chạy 2026-10-16 (commit `72f3a37`). **Chưa dùng trong bài cho đến khi chạy lại và khớp** (xem mục "Kiểm chứng chạy lại"). Mọi câu kết luận tuân theo protocol §10: chỉ viết "khác biệt / tốt hơn" khi |Δ| ≥ 0.01 và Holm p < 0.05; ngược lại viết "no clear difference". Không so hơn/kém với số đã công bố trên dataset hoặc cách chia khác.

Nguồn bảng: `results/tables/stats_<họ>.csv`, `summary_<plan>.csv`, `descriptive_*.csv`, `kendall_tau.csv`; hình: `results/figures/delta_<họ>.png`. Metric chính: macro-F1, trung bình 5 seed × 5 fold (25 fold); Δ = A − B; CI 95% chưa hiệu chỉnh; corrected repeated k-fold t-test + Holm theo họ.

## 5.0 Setup (1 đoạn, nhắc lại ngắn)
PROMISE_exp (969 dòng, 47 project, 444 FR / 525 NFR, 12 lớp), 8 nhóm câu trùng (16 dòng); Dalpiaz2019 (327 dòng; 187 FR / 140 NFR). TF-IDF (1,2)-gram `min_df=2`; M0 dummy, M1 LR, M2 SVM, M3 RF, M4 CNB, M5 Hard Voting, M6 Stacking. Seeds 42, 123, 2026, 3407, 9917.

## 5.1 RQ1 — Protocol vs. reported performance (T-bin)

**Bảng 1** — macro-F1 (mean) theo model × protocol (nguồn `summary_RQ1.csv`):

| Model | S | G-dup | G-proj |
|---|---|---|---|
| M0 | 0.351 | 0.351 | 0.352 |
| M1 | 0.876 | 0.878 | 0.694 |
| M2 | 0.893 | 0.891 | 0.722 |
| M3 | 0.851 | 0.853 | 0.661 |
| M4 | 0.889 | 0.884 | 0.755 |
| M5 | 0.882 | 0.885 | 0.705 |
| M6 | 0.891 | 0.894 | 0.749 |

**(a) Câu trùng (họ RQ1-dup, 6 test).** Δ(S − G-dup) trong [−0.003, +0.005], CI bao trọn 0, 0/6 khác biệt rõ → **kết quả âm**. Chỉ có 8 nhóm trùng (16 dòng), 6–8 nhóm vắt qua fold dưới S mỗi seed. Không dùng chữ "leakage" cho phần này (§10): viết "no measurable inflation attributable to duplicates in PROMISE_exp".
→ Hình: `delta_RQ1-dup.png`.

**(b) Project (họ RQ1-proj, 6 test).** Δ(S − G-proj) = +0.13…+0.19, Holm p ≤ 0.0073, 6/6 khác biệt rõ. SD theo fold lớn (0.05–0.11; 47 project / 5 fold). Viết là "performance drop on unseen projects", **không** khẳng định đây là rò rỉ (chưa tách được khác biệt giữa project).
→ Hình: `delta_RQ1-proj.png`. Kendall τ (S vs G-dup) = 0.73, (S vs G-proj) = 0.60 — mô tả, 6 model.

**Dalpiaz2019 (D2, mô tả — A-007/A-008):** S vs LODO (n = 25 vs 4, không ghép cặp): macro-F1 giảm 0.21–0.31; Kendall τ = 0.2 (5 model). Nguồn `descriptive_RQ1-D2_S_vs_LODO.csv`.

## 5.2 RQ2 — Oversampling before vs. inside the fold

**T-bin (họ RQ2-bin, 10 test):** Δ(BEFORE − IN-FOLD) = +0.015…+0.027, CI bao trọn 0 (trừ M2 OS-S), 0/10 khác biệt rõ sau Holm.
**T-12 (họ RQ2-12, 10 test):** Δ = +0.39…+0.49, Holm p ≈ 0, **10/10 khác biệt rõ**; BEFORE ≈ 0.95 ở mọi model.
→ Hình: `delta_RQ2-bin.png`, `delta_RQ2-12.png`.

**NONE vs IN-FOLD (chỉ mô tả, `descriptive_none_vs_infold_RQ2.csv`):** T-bin |Δ| ≤ 0.004. T-12: oversample trong fold tăng macro-F1 của M1 +0.30, M5 +0.17, M3 +0.11, M2 +0.03; M4 giảm 0.04.

**Lưu ý phải nêu ở Method / Threats:** ở BEFORE, tập đã oversample mới được chia fold nên (i) test chứa bản sao (OS-R) hoặc mẫu tổng hợp (OS-S) của dòng train, (ii) fold BEFORE và IN-FOLD chỉ trùng chỉ số (seed, fold), không trùng dòng. Phần chênh 0.4 gồm cả hai hiệu ứng, không tách được.

## 5.3 RQ3 — Hard Voting / Stacking vs. single models (họ RQ3-Gdup, RQ3-S, 8 test mỗi họ)

| So sánh | Δ G-dup | Kết luận G-dup | Δ S | Kết luận S |
|---|---|---|---|---|
| M5 vs M3 | +0.032 | M5 > M3 | +0.030 | M5 > M3 |
| M6 vs M3 | +0.042 | M6 > M3 | +0.040 | M6 > M3 |
| M5 vs M1 / M2 / M4 | +0.007 / −0.006 / +0.001 | no clear diff. | +0.006 / −0.011 / −0.007 | no clear diff. |
| M6 vs M1 / M2 / M4 | +0.017 / +0.003 / +0.010 | no clear diff. | +0.015 / −0.002 / +0.002 | no clear diff. |

Kết luận: ensemble chỉ hơn RF (M3); không vượt LR/SVM/CNB; kết luận không đổi giữa G-dup và S. SVM (M2) ngang M5/M6.

## 5.4 Replication on Dalpiaz2019 (RQ2-D2, 10 test; A-007)
BEFORE − IN-FOLD = +0.03…+0.08 (cùng chiều PROMISE_exp) nhưng 0/10 khác biệt rõ sau Holm (327 dòng, CI rộng). Viết là "same direction, not statistically supported". NONE vs IN-FOLD: |Δ| ≤ 0.027 (mô tả). Kiểm tra độ nhạy bỏ 81 câu có cả hai nhãn: chạy trong plan D2, **chưa báo cáo** — thêm bảng `summary_D2.csv` (dataset `dalpiaz_requirements_noboth.csv`, protocol S) vào phụ lục.

## 5.5 Error analysis (§11)
30 dòng (15 M2 + 15 M5; T-bin / G-dup / seed 42): `results/predictions/error_analysis_sample.csv` (không public, chứa text). Việc gán nhãn của Phat Tai còn trống → điền `phat_tai_category`, đối chiếu (và `hoang_anh_category` nếu nhờ), rồi thống kê số dòng theo nhóm cho Bảng 5. TODO.

## Việc còn thiếu trước khi viết hết Results
- [ ] Gán nhãn 30 dòng error analysis → bảng nhóm lỗi.
- [ ] Bảng phụ lục no-both (Dalpiaz).
- [ ] Hình tổng hợp (tùy chọn): macro-F1 theo model × protocol (Bảng 1 dạng hình), dùng skill dataviz.
- [ ] Bảng CI đầy đủ cho phụ lục (từ `stats_*.csv`).

## Kiểm chứng chạy lại (trước khi push và trước khi dùng số liệu)
Chạy sạch từ commit `72f3a37` (hoặc HEAD), cùng `requirements.txt` và Python 3.12:

```powershell
.venv\Scripts\python -m pytest -q tests          # kỳ vọng 34 passed
.venv\Scripts\python -m src.audit_dataset         # kỳ vọng: 969 dòng, 8 nhóm trùng, 0 xung đột; Dalpiaz 327 dòng
.venv\Scripts\python -m src.run_experiments --plan RQ1 --owner phat-tai
.venv\Scripts\python -m src.run_experiments --plan RQ2 --owner phat-tai
.venv\Scripts\python -m src.run_experiments --plan D2  --owner phat-tai
Get-FileHash results\tables\fold_scores_*.csv -Algorithm SHA256
.venv\Scripts\python -m src.analyze_results
```

Runner ghi đè `results/tables/fold_scores_*.csv` (đã commit ở `72f3a37`), nên sau khi chạy lại `git diff --stat results/tables` rỗng nghĩa là tái lập đúng từng bit (`experiment_log.csv` sẽ thêm dòng mới, bình thường). Kỳ vọng SHA-256 của `fold_scores` (lần chạy 2026-10-16) nếu kết quả tái lập đúng từng bit:

| File | SHA-256 |
|---|---|
| fold_scores_RQ1.csv | `76ce9924527ef289f2f5dc33384ae3ec03b988ae26ade9b5edfd33daf99ec706` |
| fold_scores_RQ2.csv | `d0f3e19bb35fa130f758e6eee0ade360670d5100dce2d74d81ec2564223bd3d5` |
| fold_scores_D2.csv | `af21fe05b9f2860b575401ed133033f173dd0170951b658f71e4e6c326b50432` |

Nếu hash khác: so từng ô `macro_f1` (file CSV), ghi chênh lệch lớn nhất vào `research_log.md`; chênh ≤ 1e-9 (sai số số học) thì coi là tái lập; chênh lớn hơn thì **không sửa/chọn lại**, ghi nguyên nhân (phiên bản gói, thứ tự dữ liệu) và báo cáo cả hai lần chạy. Không chạy lại để "đẹp" kết quả (§Key constraints).
Sau khi khớp: ghi thời gian + kết quả vào `research_log.md`, rồi mới push.

### Kết quả kiểm chứng chạy lại (2026-10-18, Phat Tai, máy cá nhân)

`pytest` 34 passed; `audit_dataset` khớp; 3 hash `fold_scores_{RQ1,RQ2,D2}.csv` trùng khớp bảng trên, `git diff --stat results/tables` rỗng → **tái lập đúng từng bit**. Số "clear differences" giống lần đầu. Thời gian: RQ1 413 s, RQ2 710 s, D2 174 s (lần đầu 398/611/150 s). `results/splits/splits_D2.csv` chỉ khác thứ tự khối dataset (cùng nội dung sau khi sắp xếp) do duyệt `set` tên file trong `run_experiments.py`; đã sửa thành `sorted(...)` (chỉ ảnh hưởng thứ tự ghi file, không đổi thiết kế) và khôi phục file đã commit.
