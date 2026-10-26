# Kế hoạch slide (16:9, chữ trên slide bằng tiếng Anh)

**Cập nhật:** 26/10/2026, theo bài báo ở commit `490af74`. Bộ slide được sắp theo **5 nội dung trọng tâm**.
**Số slide:** 19. **Thời lượng mục tiêu:** khoảng 18 phút.
**Nguồn số liệu duy nhất:** `paper/fact_sheet.md` và `paper/tables/*.tex`.

## Cấu trúc 5 phần

| Phần | Nội dung trọng tâm | Slide | Người trình bày |
|---|---|---|---|
| I | Background and significance (Bối cảnh và ý nghĩa) | 1–3 | Phát Tài |
| II | State of research (Thực trạng nghiên cứu) | 4 | Phát Tài |
| III | Research content and method (Nội dung và phương pháp), kèm kết quả | 5–16 | Phát Tài: 5, 9–13 · Hoàng Ánh: 6–8, 14–16 |
| IV | Novelty (Điểm mới của nghiên cứu) | 17 | Phát Tài |
| V | Conclusion and summary (Kết luận và tóm tắt) | 18–19 | Phát Tài |

Mỗi slide có một nhãn phần nhỏ ở góc trên (ví dụ "I · Background") để người nghe biết đang ở phần nào.

## Quy tắc trình bày

1. Mỗi slide một ý, chữ trên màn hình tối đa khoảng 35 từ (không tính bảng); phần giải thích đặt trong speaker notes.
2. Bảng quá dài thì tách sang slide kế tiếp, tối đa 2 slide (chỉ RQ2 dùng 2 slide).
3. Theo A-009: RQ1, RQ2 và Dalpiaz chỉ là **mô tả**. Không ghi "significant", "clear difference", "6/6", "10/10" cho các phần này. Chỉ RQ3 (slide 14) được nói "clearly better" / "no clear difference".
4. Không gọi RQ1(b) (dự án mới) là "leakage". Không nói các bài 98–99% là sai.

## Hình có sẵn

| File | Slide |
|---|---|
| `paper/figures/summary_deltas.png` | 9 |
| `paper/figures/slide_rq2_t12.png` | 12 |
| Fig. 1 của bài (chụp từ PDF) hoặc vẽ lại theo `paper/figures/design.tex` | 7 |

---

## Nội dung từng slide

### Slide 1. How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification?
Section: I · Background and significance
A Leakage-Aware Re-Evaluation of Single and Ensemble Classifiers
Tai Nguyen Phat · Anh Hoang
FPT University HCMC · SWR302
Visual: title slide, dark background.
Notes: Nhóm kiểm tra xem các điểm số rất cao trong phân loại yêu cầu phần mềm đến từ mô hình tốt hay từ cách đánh giá chưa chặt.
Người / thời gian: Phát Tài · 0.5 phút

### Slide 2. Background: classifying FR and NFR
Section: I · Background and significance
- FR: what the system does. "New users can sign up by creating new ID."
- NFR: how well it does it. "The system shall utilize HTTPS communication to ensure data confidentiality."
- Automatic classification helps plan architecture, testing and QA early
- Studied since at least 2007; most studies use the PROMISE NFR dataset
Visual: two cards, FR and NFR.
Notes: Bài toán có hai mức: T-bin (FR và NFR) và T-12 (12 loại như security, usability, performance). Đây là bài toán quen thuộc trong kỹ thuật yêu cầu.
Người / thời gian: Phát Tài · 1 phút

### Slide 3. Significance: are high scores real?
Section: I · Background and significance
- 98.79% accuracy (Metu et al., 2024)
- 99% accuracy (Baskoro et al., 2021)
- If the evaluation inflates scores, teams may pick the wrong model and trust it too much
- Question: are we measuring the model, or the evaluation?
Visual: two big numbers, one question box.
Notes: Ý nghĩa của đề tài: nếu điểm số bị thổi phồng do cách đánh giá, người làm nghiên cứu và người dùng thực tế sẽ đánh giá sai mô hình. Nhóm không nói các bài 98–99% là sai, chỉ đặt câu hỏi.
Người / thời gian: Phát Tài · 1 phút

### Slide 4. State of research: what 21 studies do
Section: II · State of research

| Practice | Studies |
|---|---|
| Random split, duplicates not handled | 14 / 21 |
| Oversampling before splitting | 3 of 6 that oversample |
| Ensemble gains claimed without a test | 4 of 6 ensemble studies |
| Report macro-F1 | 1 / 21 |
| Test on unseen projects | 3 / 21 |
| Publish code and data | 5 / 21 |

- Gap: no study measures how much these choices change the scores
Visual: table, first three rows highlighted.
Notes: Nhóm chọn có hệ thống 30 bài, giữ 21 nghiên cứu thực nghiệm. Ba dòng đầu là ba thực hành bài này đo trực tiếp. Khoảng trống: nhóm không tìm thấy nghiên cứu nào đo mức ảnh hưởng của chúng trong phân loại FR/NFR.
Người / thời gian: Phát Tài · 1.5 phút

### Slide 5. Research content: three questions
Section: III · Content and method
- RQ1: Do scores change if duplicates (a) or whole projects (b) stay in one fold?
- RQ2: How much does oversampling before splitting inflate scores?
- RQ3: Do hard voting and stacking beat single classifiers?
Visual: three cards.
Notes: Mỗi RQ ứng với một thực hành ở slide 4. RQ1(a) và RQ2 là câu hỏi về rò rỉ dữ liệu; RQ1(b) là khả năng dùng cho dự án mới.
Người / thời gian: Phát Tài · 1 phút

### Slide 6. Method: data
Section: III · Content and method
- PROMISE_exp: 969 requirements (444 FR, 525 NFR), 47 projects, 12 classes
- 8 duplicate groups (16 rows)
- Replication: Dalpiaz et al., 327 requirements (187 FR, 140 NFR), 4 datasets
Visual: two data blocks.
Notes: Nhóm trùng gồm 3 nhóm trùng hoàn toàn và 5 cặp gần trùng (cosine ≥ 0.90, kiểm tra tay). Lớp hiếm nhất PO chỉ có 12 câu, lớp F có 444 câu, điều này quan trọng cho RQ2.
Người / thời gian: Hoàng Ánh · 1 phút

### Slide 7. Method: evaluation design
Section: III · Content and method
Splitting protocols:
- S: stratified random 5-fold CV
- G-dup: duplicates kept in one fold
- G-proj: each project kept in one fold

Oversampling order:
- BEFORE: oversample all rows, then split
- IN-FOLD: split, then oversample training rows only

5 seeds × 5 folds = 25 fold scores per configuration
Visual: left column protocols, right column oversampling order.
Notes: Với BEFORE, bản sao của một câu có thể nằm ở cả tập train và tập test.
Người / thời gian: Hoàng Ánh · 1.5 phút

### Slide 8. Method: models and how we compare
Section: III · Content and method
- Text → TF-IDF (fitted on the training fold only) → classifier
- M0 dummy, M1 LR, M2 SVM, M3 RF, M4 CNB; ensembles M5 voting, M6 stacking
- Same test folds (RQ3): corrected t-test + Holm
- Different test folds (RQ1, RQ2): mean, SD and Δ only
- Protocol locked before any run; no re-runs
Visual: pipeline on top, two columns "test" vs "describe" below.
Notes: Mô hình cố định, không tinh chỉnh. S và G-dup/G-proj trùng 0/25 test fold; test fold của BEFORE có 210–1066 dòng so với 193–194, nên RQ1, RQ2 chỉ báo cáo mô tả (amendment A-009, không chạy lại mô hình).
Người / thời gian: Hoàng Ánh · 1.5 phút

### Slide 9. Results at a glance
Section: III · Content and method
- Two large effects: unseen projects and BEFORE on 12 classes
- Ensembles: clearly better than random forest only
Visual: summary_deltas.png large.
Notes: Dấu × là so sánh mô tả, chấm tròn là RQ3 có kiểm định. Hai cụm xa 0 nhất là G-proj (0.13–0.19) và T-12 (0.39–0.49).
Người / thời gian: Phát Tài · 1 phút

### Slide 10. RQ1: duplicates and unseen projects
Section: III · Content and method

| Model | S | G-dup | G-proj | S − G-proj |
|---|---|---|---|---|
| M1 LR | 0.876 | 0.878 | 0.694 | +0.182 |
| M2 SVM | 0.893 | 0.891 | 0.722 | +0.171 |
| M3 RF | 0.851 | 0.853 | 0.661 | +0.190 |
| M4 CNB | 0.889 | 0.884 | 0.755 | +0.134 |
| M5 Voting | 0.882 | 0.885 | 0.705 | +0.176 |
| M6 Stacking | 0.891 | 0.894 | 0.749 | +0.142 |

- Duplicates: change < 0.01 (only 8 groups)
- Unseen projects: −0.134 to −0.190; best model changes from M2 to M4
Notes: G-dup gần như không đổi vì chỉ có 8 nhóm trùng. G-proj giảm rõ, xếp hạng đổi (Kendall τ = 0.600). Không gọi là leakage.
Người / thời gian: Phát Tài · 1.5 phút

### Slide 11. RQ2 (1/2): binary task
Section: III · Content and method

| Model | BEFORE | IN-FOLD | Δ |
|---|---|---|---|
| M1 LR | 0.899 | 0.878 | +0.020 |
| M2 SVM | 0.917 | 0.893 | +0.024 |
| M3 RF | 0.882 | 0.855 | +0.027 |
| M4 CNB | 0.903 | 0.888 | +0.015 |
| M5 Voting | 0.909 | 0.886 | +0.023 |

- Always higher, but small: same size as the variation between folds
- Note: random oversampling; SMOTE gives +0.015 to +0.026
Notes: T-bin gần cân bằng (444 vs 525) nên ít câu bị nhân bản.
Người / thời gian: Phát Tài · 1 phút

### Slide 12. RQ2 (2/2): 12 classes, the main finding
Section: III · Content and method

| Model | BEFORE | IN-FOLD | Δ |
|---|---|---|---|
| M1 LR | 0.989 | 0.597 | +0.392 |
| M2 SVM | 0.992 | 0.593 | +0.399 |
| M3 RF | 0.994 | 0.506 | +0.488 |
| M4 CNB | 0.967 | 0.526 | +0.441 |
| M5 Voting | 0.992 | 0.595 | +0.398 |

- A task near 0.6 looks like a task near 0.99
- Note: random oversampling; SMOTE gives +0.398 to +0.491
Visual: table left, slide_rq2_t12.png right.
Notes: Kết quả chính, cùng cỡ với 98–99% ở slide 3.
Người / thời gian: Phát Tài · 2 phút

### Slide 13. Why BEFORE inflates 12 classes so much
Section: III · Content and method
- Rare classes (PO: 12 rows) are copied many times to match F (444)
- Copies land in both training and test folds
- The model is tested on what it has already seen
Visual: one small box copied many times, arrows into Train and Test.
Notes: Không oversampling, T-12 đạt 0.292–0.563; oversampling đúng cách đạt 0.495–0.597. Khoảng cách tới 0.95–0.99 là do bản sao lọt vào tập test.
Người / thời gian: Phát Tài · 1 phút

### Slide 14. RQ3: do ensembles help?
Section: III · Content and method

| Comparison (G-dup) | Δ | Result |
|---|---|---|
| M5 Voting vs M3 RF | +0.032 | clearly better |
| M6 Stacking vs M3 RF | +0.042 | clearly better |
| M5 / M6 vs LR, SVM, CNB | −0.006 to +0.017 | no clear difference |

- Same pattern under stratified CV
Notes: Phần duy nhất dùng kiểm định vì các mô hình dùng chung split. M1 và M2 cùng là mô hình tuyến tính trên cùng đặc trưng nên lỗi tương quan, gộp lại ít lợi.
Người / thời gian: Hoàng Ánh · 1.5 phút

### Slide 15. Replication on Dalpiaz et al.
Section: III · Content and method
- BEFORE vs IN-FOLD: +0.034 to +0.081 (same direction, small)
- Unseen dataset (LODO): 0.405–0.511 vs 0.709–0.746 under S
- Drop of 0.21–0.31; rankings barely agree (τ = 0.20)
Visual: two big numbers "+0.03 to +0.08" and "−0.21 to −0.31".
Notes: Dữ liệu nhỏ (327 câu, 4 dataset), kết quả cùng hướng với PROMISE_exp. Tất cả là mô tả.
Người / thời gian: Hoàng Ánh · 1 phút

### Slide 16. Error analysis: why models fail
Section: III · Content and method

| Category (30 errors of M2 and M5) | Rows |
|---|---|
| Ambiguous / underspecified | 8 |
| Mixed FR/NFR | 7 |
| Functional verb in NFR | 6 |
| Quality keyword in FR | 4 |
| Other categories | 5 |

- Agreement before reconciliation: 15 / 30 (κ = 0.391); both authors used AI assistance
Visual: horizontal bar chart.
Notes: "Other categories" gồm possible annotation issue 2, other 2, short/low context 1. Ví dụ: câu HTTPS là NFR nhưng viết như một chức năng nên bị đoán là FR.
Người / thời gian: Hoàng Ánh · 1.5 phút

### Slide 17. What is new in this study
Section: IV · Novelty
- First measurement, as far as we found, of how much evaluation choices change FR/NFR scores
- Three practices tested on one fixed pipeline, two datasets, 25 folds per setting
- Paired tests only where test folds match; other comparisons descriptive
- Locked protocol, bit-identical re-run, public code, splits and fold scores
Visual: four icon cards.
Notes: Điểm mới không nằm ở mô hình mà ở cách đo. Nhóm định lượng được mức thổi phồng cho từng thực hành, và làm theo quy trình có thể kiểm chứng lại. Việc tách so sánh có kiểm định và so sánh mô tả (A-009) cũng là một điểm nhóm rút ra cho các nghiên cứu sau.
Người / thời gian: Phát Tài · 1.5 phút

### Slide 18. Conclusion and summary
Section: V · Conclusion
- Oversampling before splitting: +0.392 to +0.491 on 12 classes
- Unseen projects: −0.134 to −0.190; model ranking changes
- Duplicates: < 0.01 here; ensembles beat only random forest
- Models differ by at most 0.042; evaluation moves scores by up to 0.491

Recommendations: oversample in-fold only · group duplicates · report unseen-project results · test on the same folds · publish code and splits
Limitations: one main benchmark, classical models only
Visual: four key numbers on the left, recommendations on the right.
Notes: Thông điệp chính: cách đánh giá có thể quan trọng hơn việc chọn mô hình. Hướng tiếp theo: chạy cùng quy trình cho transformer và LLM, và cho bộ dữ liệu có nhiều câu trùng hơn.
Người / thời gian: Phát Tài · 2 phút

### Slide 19. Thank you! Questions?
Section: V · Conclusion
Code, splits and fold scores: github.com/TaiNguyen66/fr_nfr_ensemble_research
Visual: QR code to the repository.
Notes: Mời thầy cô và các bạn đặt câu hỏi.
Người / thời gian: Cả hai · 0.5 phút

---

**Tổng thời gian:** Phát Tài khoảng 11.5 phút, Hoàng Ánh khoảng 8 phút. Nếu cần về 18 phút, rút gọn phần nói ở slide 4, 7 và 8.

## Câu hỏi có thể gặp

- **Vì sao không dùng BERT/LLM?** Nghiên cứu đo ảnh hưởng của cách đánh giá, nên cần pipeline rẻ và cố định. Hướng tiếp theo là chạy cùng quy trình cho transformer và LLM.
- **Vì sao RQ1, RQ2 không có p-value?** Các cách chia tạo ra tập test khác nhau (0/25 fold trùng; BEFORE có 210–1066 dòng test). T-test ghép cặp cần cùng tập test, nên nhóm báo cáo mô tả (A-009, ghi lại và theo hướng thận trọng hơn).
- **Không có p-value thì sao biết khác biệt là thật?** So với độ dao động giữa các fold: T-12 chênh 0.39–0.49 trong khi SD chỉ 0.002–0.075; G-proj chênh 0.13–0.19. Riêng T-bin (0.015–0.027) thì nhỏ, nhóm nói rõ là yếu.
- **Điểm mới so với các bài trước là gì?** Các bài trước đề xuất mô hình mới; bài này đo xem cách đánh giá đẩy điểm lên bao nhiêu, trên cùng một pipeline cố định, và công bố toàn bộ để kiểm chứng lại.
- **Vì sao RQ1(a) không có hiệu ứng?** PROMISE_exp chỉ có 8 nhóm trùng (16/969 câu). Đây là kết quả âm trên dataset này.
- **κ = 0.391 có thấp không?** Mức vừa phải. Nhiều lỗi có hơn một nguyên nhân; nhóm đã thống nhất lại cả 30 câu và nói rõ cả hai người có dùng AI hỗ trợ.
