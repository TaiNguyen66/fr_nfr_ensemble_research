# Prompt và nội dung cho Canva AI (19 slide)

**Cập nhật:** 26/10/2026, theo bài báo ở commit `02f6129` và `SLIDES_PLAN.md`.
Mọi số liệu lấy từ `paper/fact_sheet.md`. Sau khi Canva tạo xong, **phải soát lại từng con số** với file này, vì AI có thể làm tròn hoặc tự thêm nội dung.

## Nên dùng cách nào?

| Cách | Khi nào dùng | Ưu điểm |
|---|---|---|
| **A. Docs to Deck (khuyến nghị)** | Muốn giữ đúng chữ và số | Canva dựng slide từ đúng nội dung bạn dán, ít tự bịa |
| B. Magic Design / "Create with AI" | Muốn Canva tự thiết kế nhanh | Đẹp nhanh, nhưng dễ rút gọn hoặc đổi số, phải soát kỹ hơn |

### Cách A: Docs to Deck
1. Canva → **Create a design → Doc**.
2. Dán **Phần 2 (Nội dung slide)** bên dưới vào Doc. Mỗi tiêu đề `Slide N` là một slide.
3. Trên thanh công cụ chọn **Magic Switch / Convert → Presentation** (hoặc nút **Docs to Decks**).
4. Khi Canva hỏi thêm yêu cầu, dán **Phần 1 (Prompt)**.
5. Chọn kiểu thiết kế, rồi soát theo **Phần 4 (Checklist)**.

### Cách B: Magic Design
1. Canva → **Presentations → Create with AI / Magic Design**.
2. Dán **Phần 1 (Prompt)**, rồi dán tiếp **Phần 2**.
3. Nếu Canva báo prompt quá dài, chuyển sang Cách A.

Tên nút trong Canva có thể khác tuỳ phiên bản và gói tài khoản.

---

## Phần 1. Prompt (dán vào Canva AI)

```text
Create a 19-slide academic research presentation (16:9) in English for a university software engineering course (SWR302, FPT University HCMC).

Topic: how evaluation leakage inflates functional/non-functional (FR/NFR) requirements classification results.
Authors: Tai Nguyen Phat, Anh Hoang.
Audience: lecturers and students; the talk is about 18 minutes.

Style: minimalist and clean academic. Dark teal (#0F4C5C) as the main colour, orange (#E36414) as the single accent, white background for content slides, dark teal background for the title and closing slides. Serif headings, sans-serif body text. Large readable text, plenty of white space, one idea per slide.

Strict content rules:
- Use exactly one slide per "Slide N" section of the content I provide, in the same order. Do not add, remove, merge or split slides.
- Keep the slide titles exactly as written.
- Copy every number exactly as written. Do not round, change or invent numbers.
- Show every table as a real table with exactly the rows and values given.
- Do not add facts, citations, quotes or statistics that are not in my content.
- Never write "significant", "statistically significant", "6/6" or "10/10". Only slide 15 may say "clearly better" or "no clear difference".
- Do not describe the unseen-project drop as "leakage".
- Use simple icons or shapes as visuals; leave the marked empty area on slides 10 and 13 for charts I will add myself.
- Put the speaker notes text into the slide notes, not on the slide.
```

---

## Phần 2. Nội dung slide (dán vào Canva Doc hoặc sau prompt)

### Slide 1. How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification?
A Leakage-Aware Re-Evaluation of Single and Ensemble Classifiers
Tai Nguyen Phat · Anh Hoang
FPT University HCMC · SWR302
Notes: Nhóm đo xem cách đánh giá làm điểm số phân loại FR/NFR cao lên bao nhiêu.

### Slide 2. FR or NFR?
- FR: what the system does. "New users can sign up by creating new ID."
- NFR: how well it does it. "The system shall utilize HTTPS communication to ensure data confidentiality."
- Classifying requirements automatically helps plan architecture, testing and QA.
Visual: two side-by-side cards, FR and NFR.
Notes: Có hai bài toán: T-bin (FR vs NFR) và T-12 (12 loại như security, usability, performance).

### Slide 3. Reported results look almost perfect
- 98.79% accuracy (Metu et al., 2024)
- 99% accuracy (Baskoro et al., 2021)
- Are we measuring the model, or the evaluation?
Visual: the two numbers very large, the question below.
Notes: Hai điểm cao nhất trong 21 nghiên cứu nhóm review, cả hai có dấu hiệu oversampling trước khi chia dữ liệu. Nhóm không nói hai bài đó sai.

### Slide 4. What 21 studies do

| Practice | Studies |
|---|---|
| Random split, duplicates not handled | 14 / 21 |
| Oversampling before splitting | 3 of 6 that oversample |
| Ensemble gains claimed without a test | 4 of 6 ensemble studies |
| Report macro-F1 | 1 / 21 |
| Test on unseen projects | 3 / 21 |
| Publish code and data | 5 / 21 |

Highlight the first three rows.
Notes: Nhóm chọn có hệ thống 30 bài, giữ 21 nghiên cứu thực nghiệm. Ba dòng đầu là ba thực hành bài này đo trực tiếp.

### Slide 5. Research questions
- RQ1: Do scores change if duplicates (a) or whole projects (b) stay in one fold?
- RQ2: How much does oversampling before splitting inflate scores?
- RQ3: Do hard voting and stacking beat single classifiers?
Visual: three cards.
Notes: RQ1(a) và RQ2 là câu hỏi về leakage. RQ1(b) là khả năng tổng quát hoá sang dự án mới.

### Slide 6. Data
- PROMISE_exp: 969 requirements (444 FR, 525 NFR), 47 projects, 12 classes
- 8 duplicate groups (16 rows)
- Replication: Dalpiaz et al., 327 requirements (187 FR, 140 NFR), 4 datasets
Visual: two data blocks.
Notes: Lớp hiếm nhất PO chỉ có 12 câu, lớp F có 444 câu. Điều này quan trọng cho RQ2.

### Slide 7. Evaluation design
Splitting protocols:
- S: stratified random 5-fold CV
- G-dup: duplicates kept in one fold
- G-proj: each project kept in one fold

Oversampling order:
- BEFORE: oversample all rows, then split
- IN-FOLD: split, then oversample training rows only

5 seeds × 5 folds = 25 scores per configuration
Visual: left column for protocols, right column for oversampling order.
Notes: Với BEFORE, bản sao của một câu có thể nằm ở cả tập train và tập test.

### Slide 8. Models and pipeline
- Text → TF-IDF (1–2 grams, fitted on the training fold only) → Classifier
- Single: M0 dummy, M1 logistic regression, M2 linear SVM, M3 random forest, M4 complement NB
- Ensembles: M5 hard voting, M6 stacking (both of M1–M3)
- Fixed hyperparameters, no tuning
Visual: three-step pipeline diagram.
Notes: Mô hình cổ điển và cố định từ đầu, vì mục tiêu là đo ảnh hưởng của cách đánh giá. M0 là mốc sàn, macro-F1 khoảng 0.35.

### Slide 9. How we compare
- Same test folds → test (RQ3): corrected t-test + Holm; clear = |Δ| ≥ 0.01 and p < 0.05
- Different test folds → describe (RQ1, RQ2, replication): mean, SD and Δ only
- Protocol locked before any run; no configuration re-run
Visual: two columns.
Notes: S và G-dup/G-proj trùng 0/25 test fold; test fold của BEFORE có 210–1066 dòng so với 193–194. Không ghép cặp được nên RQ1, RQ2 chỉ báo cáo mô tả (sửa đổi A-009, không chạy lại mô hình).

### Slide 10. Results at a glance
- Two large effects: unseen projects and BEFORE on 12 classes
- Ensembles: clearly better than random forest only
Visual: leave a large empty area on the left for a chart (summary_deltas.png).
Notes: Dấu × là so sánh mô tả, chấm tròn là RQ3 có kiểm định. Hai cụm xa 0 nhất là G-proj (0.13–0.19) và T-12 (0.39–0.49).

### Slide 11. RQ1: duplicates and unseen projects

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
Notes: G-dup gần như không đổi vì chỉ có 8 nhóm trùng. G-proj giảm rõ, xếp hạng thay đổi (Kendall τ = 0.600). Không gọi là leakage.

### Slide 12. RQ2 (1/2): binary task

| Model | BEFORE | IN-FOLD | Δ |
|---|---|---|---|
| M1 LR | 0.899 | 0.878 | +0.020 |
| M2 SVM | 0.917 | 0.893 | +0.024 |
| M3 RF | 0.882 | 0.855 | +0.027 |
| M4 CNB | 0.903 | 0.888 | +0.015 |
| M5 Voting | 0.909 | 0.886 | +0.023 |

- Always higher, but small: same size as the variation between folds
- Small note: random oversampling; SMOTE gives +0.015 to +0.026
Notes: T-bin gần cân bằng (444 vs 525) nên ít câu bị nhân bản.

### Slide 13. RQ2 (2/2): 12 classes, the main finding

| Model | BEFORE | IN-FOLD | Δ |
|---|---|---|---|
| M1 LR | 0.989 | 0.597 | +0.392 |
| M2 SVM | 0.992 | 0.593 | +0.399 |
| M3 RF | 0.994 | 0.506 | +0.488 |
| M4 CNB | 0.967 | 0.526 | +0.441 |
| M5 Voting | 0.992 | 0.595 | +0.398 |

- A task near 0.6 looks like a task near 0.99
- Small note: random oversampling; SMOTE gives +0.398 to +0.491
Visual: table on the left, empty area on the right for a chart (slide_rq2_t12.png).
Notes: Đây là kết quả chính, cùng cỡ với các con số 98–99% ở slide 3.

### Slide 14. Why BEFORE inflates 12 classes so much
- Rare classes (PO: 12 rows) are copied many times to match F (444)
- Copies land in both training and test folds
- The model is tested on what it has already seen
Visual: one small box copied several times, arrows into "Train" and "Test".
Notes: Không oversampling, T-12 đạt 0.292–0.563; oversampling đúng cách đạt 0.495–0.597. Khoảng cách tới 0.95–0.99 là do bản sao lọt vào tập test.

### Slide 15. RQ3: do ensembles help?

| Comparison (G-dup) | Δ | Result |
|---|---|---|
| M5 Voting vs M3 RF | +0.032 | clearly better |
| M6 Stacking vs M3 RF | +0.042 | clearly better |
| M5 / M6 vs LR, SVM, CNB | −0.006 to +0.017 | no clear difference |

- Same pattern under stratified CV
Notes: Phần duy nhất dùng kiểm định vì các mô hình dùng chung split. M1 và M2 cùng là mô hình tuyến tính nên lỗi tương quan, gộp lại ít lợi.

### Slide 16. Replication on Dalpiaz et al.
- BEFORE vs IN-FOLD: +0.034 to +0.081 (same direction, small)
- Unseen dataset (LODO): 0.405–0.511 vs 0.709–0.746 under S
- Drop of 0.21–0.31; rankings barely agree (τ = 0.20)
Visual: two big numbers: "+0.03 to +0.08" and "−0.21 to −0.31".
Notes: Dữ liệu nhỏ (327 câu, 4 dataset), kết quả cùng hướng với PROMISE_exp. Tất cả là mô tả.

### Slide 17. Error analysis: why models fail

| Category (30 errors of M2 and M5) | Rows |
|---|---|
| Ambiguous / underspecified | 8 |
| Mixed FR/NFR | 7 |
| Functional verb in NFR | 6 |
| Quality keyword in FR | 4 |
| Other categories | 5 |

- Agreement before reconciliation: 15 / 30 (κ = 0.391)
- Both authors used AI assistance while labelling
Visual: horizontal bar chart of the table.
Notes: "Other categories" gồm possible annotation issue 2, other 2, short/low context 1. Ví dụ: câu HTTPS là NFR nhưng viết như một chức năng nên bị đoán là FR.

### Slide 18. Limitations and recommendations
Limitations: one main benchmark · classical models only · fixed hyperparameters · 30-row error analysis

Recommendations:
1. Oversample inside the training fold only
2. Group duplicates and report how many
3. Report unseen-project results
4. Use corrected tests on the same folds
5. Publish code, splits and fold scores
Notes: Trên T-bin các mô hình chỉ chênh nhau tối đa 0.042, nhưng cách đánh giá làm điểm thay đổi tới 0.190 (dự án mới) và 0.491 (BEFORE trên 12 lớp).

### Slide 19. Thank you! Questions?
Code, splits and fold scores: github.com/TaiNguyen66/fr_nfr_ensemble_research
Visual: QR code to the repository.

---

## Phần 3. Sau khi Canva tạo xong

1. Chèn hình: tải `paper/figures/summary_deltas.png` vào slide 10 và `paper/figures/slide_rq2_t12.png` vào slide 13.
2. Tạo mã QR cho slide 19: Canva → **Apps → QR Code**, nhập link GitHub.
3. Kiểm tra speaker notes; nếu Canva không đưa vào phần *Notes*, chép từ Phần 2.

## Phần 4. Checklist soát lỗi

- [ ] Đủ 19 slide, đúng thứ tự, đúng tiêu đề.
- [ ] Mọi số trong bảng slide 4, 11, 12, 13, 15, 17 khớp từng chữ số với Phần 2.
- [ ] Không có chữ "significant", "6/6", "10/10" ở bất kỳ đâu.
- [ ] Chỉ slide 15 có "clearly better" / "no clear difference".
- [ ] Không có câu, trích dẫn hay con số nào Canva tự thêm.
- [ ] Hai hình kết quả đã chèn ở slide 10 và 13.
- [ ] Tên tác giả và link GitHub đúng.
