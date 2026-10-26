# Kế hoạch slide (Gemini + Canva, 16:9, chữ trên slide bằng tiếng Anh)

**Cập nhật:** 26/10/2026, theo bài báo ở commit `02f6129` (A-009 và Error analysis đã thống nhất).
**Số slide:** 19 (18 slide nội dung + 1 slide cảm ơn/Q&A). **Thời lượng mục tiêu:** khoảng 18 phút.
**Nguồn số liệu duy nhất:** `paper/fact_sheet.md` và `paper/tables/*.tex`. Không thêm số nào không có ở đó.

## Quy tắc trình bày

1. Mỗi slide một ý. Chữ trên màn hình tối đa khoảng 35 từ (không tính bảng); phần giải thích đặt trong *Speaker notes*.
2. Bảng kết quả quá dài thì tách sang slide kế tiếp, tối đa 2 slide cho một bảng (ở đây chỉ RQ2 cần 2 slide).
3. Số làm tròn 3 chữ số như trong bài; khoảng số viết "0.134 to 0.190" hoặc "0.13–0.19" thống nhất trong cả bộ slide.
4. Theo A-009: RQ1, RQ2 và Dalpiaz chỉ là **mô tả** (difference of means). **Không** ghi "significant", "clear difference", "6/6", "10/10", "p-value" cho các phần này. Chỉ RQ3 được nói "clearly better" / "no clear difference".
5. Không gọi RQ1(b) (unseen projects) là "leakage".
6. Không nói các bài báo 98–99% là sai; chỉ nói BEFORE đủ để tạo ra con số cỡ đó.

## Hình có sẵn

| File | Dùng ở slide |
|---|---|
| `paper/figures/summary_deltas.png` | 10 |
| `paper/figures/slide_rq2_t12.png` | 13 |
| Sơ đồ thiết kế: chụp Fig. 1 từ PDF Overleaf, hoặc vẽ lại bằng shape Canva theo `paper/figures/design.tex` | 7 |

Các hình cũ `results/figures/delta_RQ1-*.png`, `delta_RQ2-*.png` **đã bị xoá theo A-009, không dùng**.

## Phân công (đề xuất, Phát Tài quyết định)

- Phát Tài: slide 1–5, 10–14, 18–19.
- Hoàng Ánh: slide 6–9, 15–17.

---

## Nội dung từng slide

### Slide 1. Title
**On slide**
- How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification?
- A Leakage-Aware Re-Evaluation of Single and Ensemble Classifiers
- Tai Nguyen Phat, Anh Hoang · FPT University HCMC · SWR302 · [ngày trình bày]

**Visual:** tiêu đề lớn, nền sáng, không hình.
**Notes (VI):** Giới thiệu nhóm và đề tài trong 1 câu: nhóm đo xem cách đánh giá làm điểm số phân loại FR/NFR cao lên bao nhiêu.
**Người / thời gian:** Phát Tài · 0.5 phút

### Slide 2. FR or NFR?
**On slide**
- **FR:** what the system does. *"New users can sign up by creating new ID."*
- **NFR:** how well it does it. *"The system shall utilize HTTPS communication to ensure data confidentiality."*
- Classifying them automatically helps plan architecture, testing and QA.

**Visual:** hai thẻ cạnh nhau (FR / NFR), mỗi thẻ một câu ví dụ (cả hai câu lấy từ PROMISE_exp).
**Notes (VI):** Giải thích bài toán. Có hai mức: T-bin (FR vs NFR) và T-12 (12 loại: security, usability, performance…).
**Người / thời gian:** Phát Tài · 1 phút

### Slide 3. Reported results look almost perfect
**On slide**
- **98.79%** accuracy (Metu et al., 2024)
- **99%** (Baskoro et al., 2021)
- Are we measuring the model, or the evaluation?

**Visual:** hai con số rất lớn, câu hỏi bên dưới.
**Notes (VI):** Hai điểm cao nhất trong 21 nghiên cứu nhóm review. Cả hai có dấu hiệu oversampling trước khi chia dữ liệu. Nhấn mạnh: nhóm không nói hai bài đó sai, chỉ đặt câu hỏi.
**Người / thời gian:** Phát Tài · 1 phút

### Slide 4. What 21 studies do
**On slide**

| Practice | Studies |
|---|---|
| Random split, duplicates not handled | 14 / 21 |
| Oversampling before splitting | 3 of 6 that oversample |
| Ensemble gains claimed without a test | 4 of 6 ensemble studies |
| Report macro-F1 | 1 / 21 |
| Test on unseen projects | 3 / 21 |
| Publish code and data | 5 / 21 |

**Visual:** bảng 6 dòng, tô nhấn 3 dòng đầu (liên quan RQ1, RQ2, RQ3).
**Notes (VI):** Nhóm chọn có hệ thống 30 bài, giữ 21 nghiên cứu thực nghiệm sau khi cả hai người kiểm tra. Ba dòng đầu là ba thực hành bài này đo trực tiếp.
**Người / thời gian:** Phát Tài · 1.5 phút

### Slide 5. Research questions
**On slide**
- **RQ1** Do scores change if duplicates (a) or whole projects (b) stay in one fold?
- **RQ2** How much does oversampling *before* splitting inflate scores?
- **RQ3** Do hard voting and stacking beat single classifiers?

**Visual:** 3 thẻ ngang, mỗi thẻ một RQ.
**Notes (VI):** RQ1(a) và RQ2 là câu hỏi về leakage. RQ1(b) là khả năng tổng quát hoá sang dự án mới, không phải leakage.
**Người / thời gian:** Phát Tài · 1 phút

### Slide 6. Data
**On slide**
- **PROMISE_exp:** 969 requirements (444 FR, 525 NFR), 47 projects, 12 classes
- 8 duplicate groups (16 rows)
- **Replication:** Dalpiaz et al., 327 requirements (187 FR, 140 NFR), 4 datasets

**Visual:** hai khối dữ liệu; có thể thêm biểu đồ cột phân bố 12 lớp (F 444, SE 125, US 85, O 77, PE 67, LF 49, A 31, MN 24, SC 22, FT 18, L 15, PO 12).
**Notes (VI):** Nhóm trùng gồm 3 nhóm trùng hoàn toàn và 5 cặp gần trùng (cosine ≥ 0.90, kiểm tra tay). Lớp hiếm nhất PO chỉ có 12 câu, điều này quan trọng cho RQ2.
**Người / thời gian:** Hoàng Ánh · 1 phút

### Slide 7. Evaluation design
**On slide**
- **S:** stratified random 5-fold CV
- **G-dup:** duplicates kept in one fold
- **G-proj:** each project kept in one fold
- **BEFORE:** oversample all rows, then split
- **IN-FOLD:** split, then oversample training rows only

**Visual:** Fig. 1 của bài (chụp từ PDF) hoặc vẽ lại: bên trái 3 ô S / G-dup / G-proj; bên phải 2 dòng BEFORE / IN-FOLD.
**Notes (VI):** Chỉ vào dòng BEFORE: sau khi nhân bản rồi mới chia, bản sao của một câu có thể nằm ở cả train và test. Mỗi cấu hình chạy 5 seed × 5 fold = 25 điểm.
**Người / thời gian:** Hoàng Ánh · 1.5 phút

### Slide 8. Models and pipeline
**On slide**
- TF-IDF (1–2 grams), fitted on the training fold only
- M0 dummy · M1 logistic regression · M2 linear SVM · M3 random forest · M4 complement NB
- M5 hard voting · M6 stacking (of M1–M3)
- Fixed hyperparameters, no tuning

**Visual:** sơ đồ pipeline 3 bước: Text → TF-IDF → Classifier.
**Notes (VI):** Mô hình cổ điển và cố định từ đầu, vì mục tiêu là đo ảnh hưởng của cách đánh giá chứ không tìm mô hình tốt nhất. M0 là mốc sàn (macro-F1 ≈ 0.35).
**Người / thời gian:** Hoàng Ánh · 1 phút

### Slide 9. How we compare
**On slide**
- Protocol locked before any run; no re-runs
- **Same splits (RQ3):** corrected t-test + Holm; "clear" = |Δ| ≥ 0.01 and p < 0.05
- **Different splits (RQ1, RQ2):** descriptive only (mean, SD, Δ)

**Visual:** hai cột: "Same test folds → test" và "Different test folds → describe".
**Notes (VI):** Giải thích A-009: S và G-dup/G-proj trùng 0/25 test fold; test fold của BEFORE có 210–1066 dòng so với 193–194. Không ghép cặp được nên không dùng t-test cho RQ1, RQ2. Đây là sửa đổi được ghi lại, theo hướng thận trọng hơn, không chạy lại mô hình.
**Người / thời gian:** Hoàng Ánh · 1.5 phút

### Slide 10. Results at a glance
**On slide**
- Two large effects: **unseen projects** and **BEFORE on 12 classes**
- Ensembles: clearly better than random forest only

**Visual:** `summary_deltas.png` chiếm phần lớn slide.
**Notes (VI):** Dấu × là so sánh mô tả; chấm tròn là RQ3 có kiểm định. Hai cụm nằm xa 0 nhất là G-proj (≈ 0.13–0.19) và T-12 (≈ 0.39–0.49).
**Người / thời gian:** Phát Tài · 1 phút

### Slide 11. RQ1: duplicates and unseen projects
**On slide**

| Model | S | G-dup | G-proj | S − G-proj |
|---|---|---|---|---|
| M1 LR | 0.876 | 0.878 | 0.694 | +0.182 |
| M2 SVM | 0.893 | 0.891 | 0.722 | +0.171 |
| M3 RF | 0.851 | 0.853 | 0.661 | +0.190 |
| M4 CNB | 0.889 | 0.884 | 0.755 | +0.134 |
| M5 Voting | 0.882 | 0.885 | 0.705 | +0.176 |
| M6 Stacking | 0.891 | 0.894 | 0.749 | +0.142 |

- Duplicates: change < 0.01 (only 8 groups)
- Unseen projects: −0.134 to −0.190; best model changes (M2 → M4)

**Visual:** bảng, tô cột G-proj; tô ô cao nhất của cột S (M2) và G-proj (M4).
**Notes (VI):** G-dup gần như không đổi vì PROMISE_exp chỉ có 8 nhóm trùng; đây là kết quả âm trên dataset này. G-proj giảm rõ, fold dao động mạnh hơn (SD 0.052–0.113 so với 0.018–0.031), xếp hạng đổi (Kendall τ = 0.600). Không gọi là leakage.
**Người / thời gian:** Phát Tài · 1.5 phút

### Slide 12. RQ2 (1/2): binary task
**On slide**

| Model | BEFORE | IN-FOLD | Δ |
|---|---|---|---|
| M1 LR | 0.899 | 0.878 | +0.020 |
| M2 SVM | 0.917 | 0.893 | +0.024 |
| M3 RF | 0.882 | 0.855 | +0.027 |
| M4 CNB | 0.903 | 0.888 | +0.015 |
| M5 Voting | 0.909 | 0.886 | +0.023 |

*Random oversampling (OS-R); SMOTE gives +0.015 to +0.026.*
- Always higher, but small: same size as fold-to-fold variation

**Visual:** bảng nhỏ, cột Δ tô màu nhạt.
**Notes (VI):** T-bin gần cân bằng (444 vs 525) nên ít câu bị nhân bản, độ chênh 0.015–0.027, cùng cỡ với SD giữa các fold (0.015–0.032).
**Người / thời gian:** Phát Tài · 1 phút

### Slide 13. RQ2 (2/2): 12 classes, the main finding
**On slide**

| Model | BEFORE | IN-FOLD | Δ |
|---|---|---|---|
| M1 LR | 0.989 | 0.597 | +0.392 |
| M2 SVM | 0.992 | 0.593 | +0.399 |
| M3 RF | 0.994 | 0.506 | +0.488 |
| M4 CNB | 0.967 | 0.526 | +0.441 |
| M5 Voting | 0.992 | 0.595 | +0.398 |

*OS-R; SMOTE gives +0.398 to +0.491.*
- A ~0.6 task looks like a ~0.99 task

**Visual:** `slide_rq2_t12.png` bên phải, bảng bên trái (hoặc chỉ dùng hình nếu chật).
**Notes (VI):** Đây là kết quả chính. BEFORE 0.951–0.994 so với IN-FOLD 0.495–0.597. Con số này cùng cỡ với 98–99% ở slide 3.
**Người / thời gian:** Phát Tài · 2 phút

### Slide 14. Why BEFORE inflates 12 classes so much
**On slide**
- Rare classes (PO: 12 rows) are copied many times to match F (444)
- Copies land in both training and test folds
- The model is tested on what it has already seen

**Visual:** minh hoạ đơn giản: 1 câu PO nhân thành nhiều bản, mũi tên chia vào Train và Test.
**Notes (VI):** Nếu oversampling đúng cách (IN-FOLD), T-12 chỉ đạt 0.495–0.597; không oversampling đạt 0.292–0.563. Khoảng cách tới 0.95–0.99 không phải do oversampling có ích mà do bản sao lọt vào tập test.
**Người / thời gian:** Phát Tài · 1 phút

### Slide 15. RQ3: do ensembles help?
**On slide**

| Comparison (G-dup) | Δ | Result |
|---|---|---|
| M5 Voting vs M3 RF | +0.032 | clearly better |
| M6 Stacking vs M3 RF | +0.042 | clearly better |
| M5 / M6 vs LR, SVM, CNB | −0.006 to +0.017 | no clear difference |

- Same pattern under stratified CV

**Visual:** bảng 3 dòng, tô 2 dòng đầu.
**Notes (VI):** Đây là phần duy nhất dùng kiểm định (corrected t-test + Holm) vì các mô hình dùng chung split. Ensemble chỉ hơn RF; với các mô hình tuyến tính thì không khác rõ, có thể do M1 và M2 cùng là mô hình tuyến tính trên cùng đặc trưng nên lỗi tương quan.
**Người / thời gian:** Hoàng Ánh · 1.5 phút

### Slide 16. Replication on Dalpiaz et al.
**On slide**
- BEFORE vs IN-FOLD: +0.034 to +0.081 (same direction, small)
- Unseen dataset (LODO): 0.405–0.511 vs 0.709–0.746 under S
- Drop of 0.21–0.31; rankings barely agree (τ = 0.20)

**Visual:** 2 cột số lớn: "BEFORE +0.03 to +0.08" và "Unseen dataset −0.21 to −0.31".
**Notes (VI):** Dữ liệu nhỏ (327 câu, 4 dataset), kết quả cùng hướng với PROMISE_exp. Tất cả là mô tả.
**Người / thời gian:** Hoàng Ánh · 1 phút

### Slide 17. Error analysis: why models fail
**On slide**

| Category (30 errors, M2 + M5) | Rows |
|---|---|
| Ambiguous / underspecified | 8 |
| Mixed FR/NFR | 7 |
| Functional verb in NFR | 6 |
| Quality keyword in FR | 4 |
| Other categories | 5 |

- Agreement before reconciliation: 15/30 (κ = 0.391)

**Visual:** biểu đồ cột ngang 5 thanh, hoặc bảng.
**Notes (VI):** 30 câu phân loại sai (T-bin, G-dup, seed 42). "Other categories" gồm possible annotation issue 2, other 2, short/low context 1. Ví dụ: câu HTTPS là NFR nhưng viết như một chức năng nên bị đoán là FR. Cả hai người có dùng AI hỗ trợ khi gán nhãn, nên mức đồng thuận không phải của hai người hoàn toàn độc lập.
**Người / thời gian:** Hoàng Ánh · 1.5 phút

### Slide 18. Limitations and recommendations
**On slide**

*Limitations:* one main benchmark · classical models only · fixed hyperparameters · 30-row error analysis

*Recommendations:*
1. Oversample inside the training fold only
2. Group duplicates and report how many
3. Report unseen-project results
4. Use corrected tests on the same folds
5. Publish code, splits and fold scores

**Visual:** hai cột: Limitations (trái, nhỏ) và Recommendations (phải, nổi bật).
**Notes (VI):** Nói nhanh giới hạn, tập trung vào 5 khuyến nghị. Câu kết: trên T-bin các mô hình chỉ chênh nhau tối đa 0.042, nhưng cách đánh giá làm điểm thay đổi tới 0.190 (dự án mới) và 0.491 (BEFORE trên 12 lớp).
**Người / thời gian:** Phát Tài · 1.5 phút

### Slide 19. Thank you / Q&A
**On slide**
- Thank you! Questions?
- Code, splits and fold scores: github.com/TaiNguyen66/fr_nfr_ensemble_research

**Visual:** mã QR dẫn tới repo GitHub.
**Người / thời gian:** Cả hai

**Tổng thời gian:** khoảng 21 phút nếu nói đủ; cắt bớt notes ở slide 4, 7, 9 để về 18 phút.

---

## Prompt cho Gemini

Dán prompt sau vào Gemini, kèm toàn bộ phần "Nội dung từng slide" ở trên:

```text
You are helping me build a 19-slide academic presentation in Canva (16:9).
Below is my slide plan. For each slide, give me:
1) the final on-slide text (English, max ~35 words excluding tables, natural and easy to read),
2) a one-line layout suggestion for Canva,
3) speaker notes in Vietnamese, 3-5 short sentences, spoken style.

Hard rules:
- Do NOT change, round differently, or add any number. Use only numbers in the plan.
- Do NOT add citations, studies or claims that are not in the plan.
- For RQ1, RQ2 and the Dalpiaz replication, never write "significant", "clear difference",
  "p-value" or counts like "6/6" or "10/10". These comparisons are descriptive.
- Only RQ3 (slide 15) may say "clearly better" or "no clear difference".
- Do not call the unseen-project drop (RQ1b) "leakage".
- Do not say that the 98-99% studies are wrong.
- Keep tables exactly as given (you may shorten model names, not values).
- Plain wording: no hype words (groundbreaking, remarkable, crucial, robust), no em dashes in sentences.
```

## Cách làm trên Canva

1. Canva → *Presentations (16:9)* → template tối giản (từ khoá gợi ý: "minimal research", "academic"), chữ tối trên nền sáng, tối đa 2 màu nhấn.
2. Bảng: dùng *Elements → Table*, gõ đúng số từ file này; không dùng Magic Write để sinh số.
3. Hình: tải lên `summary_deltas.png` (slide 10) và `slide_rq2_t12.png` (slide 13).
4. Dán speaker notes vào phần *Notes* của từng slide.
5. Share cho Hoàng Ánh quyền *Can edit*; xuất PDF dự phòng trước buổi trình bày.
6. Soát lần cuối: mọi số trên slide khớp với `paper/fact_sheet.md`.

## Câu hỏi có thể gặp

- **Vì sao không dùng BERT/LLM?** Bài nghiên cứu cách đánh giá, nên cần pipeline rẻ và cố định. Hướng tiếp theo là chạy cùng protocol cho transformer và LLM.
- **Vì sao RQ1, RQ2 không có p-value?** Các protocol tạo ra tập test khác nhau (0/25 fold trùng; BEFORE có 210–1066 dòng test). T-test ghép cặp cần cùng tập test, nên nhóm báo cáo mô tả. Sửa đổi này (A-009) được ghi lại và theo hướng thận trọng hơn.
- **Không có p-value thì sao biết khác biệt là thật?** So với độ dao động giữa các fold: T-12 chênh 0.39–0.49 trong khi SD chỉ 0.002–0.075; G-proj chênh 0.13–0.19. Riêng T-bin (0.015–0.027) thì nhỏ, nhóm nói rõ là yếu.
- **Vì sao RQ1(a) không có hiệu ứng?** PROMISE_exp chỉ có 8 nhóm trùng (16/969 câu). Đây là kết quả âm trên dataset này.
- **κ = 0.391 có thấp không?** Mức vừa phải. Nhiều lỗi có thể giải thích bằng hơn một nguyên nhân; nhóm đã thống nhất lại cả 30 câu và nói rõ cả hai người có dùng AI hỗ trợ.
- **Corrected t-test là gì?** Các fold dùng chung dữ liệu train nên phương sai bị đánh giá thấp; Nadeau & Bengio hiệu chỉnh bằng tỉ lệ n_test/n_train.
