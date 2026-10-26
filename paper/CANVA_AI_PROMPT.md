# Prompt và nội dung cho Canva AI (19 slide)

**Cập nhật:** 26/10/2026 (bản 5 phần trọng tâm), theo bài báo ở commit `490af74` và `SLIDES_PLAN.md`.
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
Structure: five parts, I Background and significance, II State of research, III Research content and method (with results), IV Novelty, V Conclusion and summary. Show the part label from each "Section:" line small in the top corner of the slide.

Style: minimalist and clean academic. Dark teal (#0F4C5C) as the main colour, orange (#E36414) as the single accent, white background for content slides, dark teal background for the title and closing slides. Serif headings, sans-serif body text. Large readable text, plenty of white space, one idea per slide.

Strict content rules:
- Use exactly one slide per "Slide N" section of the content I provide, in the same order. Do not add, remove, merge or split slides.
- Keep the slide titles exactly as written.
- Copy every number exactly as written. Do not round, change or invent numbers.
- Show every table as a real table with exactly the rows and values given.
- Do not add facts, citations, quotes or statistics that are not in my content.
- Never write "significant", "statistically significant", "6/6" or "10/10". Only slide 14 may say "clearly better" or "no clear difference".
- Do not describe the unseen-project drop as "leakage".
- Use simple icons or shapes as visuals; leave the marked empty area on slides 9 and 12 for charts I will add myself.
- Put the speaker notes text into the slide notes, not on the slide.
```

---

## Phần 2. Nội dung slide (dán vào Canva Doc hoặc đính kèm `CANVA_SLIDE_CONTENT.docx`)

19 slides in five parts: I Background and significance (1-3), II State of research (4), III Research content and method with results (5-16), IV Novelty (17), V Conclusion and summary (18-19). One slide per "Slide N" section. "Section:" is a small label shown in the slide corner. Keep titles, wording and numbers exactly as written. "Notes" lines are speaker notes (Vietnamese), not on-slide text.

### Slide 1. How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification?
Section: I · Background and significance
A Leakage-Aware Re-Evaluation of Single and Ensemble Classifiers
Tai Nguyen Phat · Anh Hoang
FPT University HCMC · SWR302
Visual: title slide, dark background.
Notes: Nhóm kiểm tra xem các điểm số rất cao trong phân loại yêu cầu phần mềm đến từ mô hình tốt hay từ cách đánh giá chưa chặt.

### Slide 2. Background: classifying FR and NFR
Section: I · Background and significance
- FR: what the system does. "New users can sign up by creating new ID."
- NFR: how well it does it. "The system shall utilize HTTPS communication to ensure data confidentiality."
- Automatic classification helps plan architecture, testing and QA early
- Studied since at least 2007; most studies use the PROMISE NFR dataset
Visual: two cards, FR and NFR.
Notes: Bài toán có hai mức: T-bin (FR và NFR) và T-12 (12 loại như security, usability, performance). Đây là bài toán quen thuộc trong kỹ thuật yêu cầu.

### Slide 3. Significance: are high scores real?
Section: I · Background and significance
- 98.79% accuracy (Metu et al., 2024)
- 99% accuracy (Baskoro et al., 2021)
- If the evaluation inflates scores, teams may pick the wrong model and trust it too much
- Question: are we measuring the model, or the evaluation?
Visual: two big numbers, one question box.
Notes: Ý nghĩa của đề tài: nếu điểm số bị thổi phồng do cách đánh giá, người làm nghiên cứu và người dùng thực tế sẽ đánh giá sai mô hình. Nhóm không nói các bài 98–99% là sai, chỉ đặt câu hỏi.

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

### Slide 5. Research content: three questions
Section: III · Content and method
- RQ1: Do scores change if duplicates (a) or whole projects (b) stay in one fold?
- RQ2: How much does oversampling before splitting inflate scores?
- RQ3: Do hard voting and stacking beat single classifiers?
Visual: three cards.
Notes: Mỗi RQ ứng với một thực hành ở slide 4. RQ1(a) và RQ2 là câu hỏi về rò rỉ dữ liệu; RQ1(b) là khả năng dùng cho dự án mới.

### Slide 6. Method: data
Section: III · Content and method
- PROMISE_exp: 969 requirements (444 FR, 525 NFR), 47 projects, 12 classes
- 8 duplicate groups (16 rows)
- Replication: Dalpiaz et al., 327 requirements (187 FR, 140 NFR), 4 datasets
Visual: two data blocks.
Notes: Nhóm trùng gồm 3 nhóm trùng hoàn toàn và 5 cặp gần trùng (cosine ≥ 0.90, kiểm tra tay). Lớp hiếm nhất PO chỉ có 12 câu, lớp F có 444 câu, điều này quan trọng cho RQ2.

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

### Slide 8. Method: models and how we compare
Section: III · Content and method
- Text → TF-IDF (fitted on the training fold only) → classifier
- M0 dummy, M1 LR, M2 SVM, M3 RF, M4 CNB; ensembles M5 voting, M6 stacking
- Same test folds (RQ3): corrected t-test + Holm
- Different test folds (RQ1, RQ2): mean, SD and Δ only
- Protocol locked before any run; no re-runs
Visual: pipeline on top, two columns "test" vs "describe" below.
Notes: Mô hình cố định, không tinh chỉnh. S và G-dup/G-proj trùng 0/25 test fold; test fold của BEFORE có 210–1066 dòng so với 193–194, nên RQ1, RQ2 chỉ báo cáo mô tả (amendment A-009, không chạy lại mô hình).

### Slide 9. Results at a glance
Section: III · Content and method
- Two large effects: unseen projects and BEFORE on 12 classes
- Ensembles: clearly better than random forest only
Visual: summary_deltas.png large.
Notes: Dấu × là so sánh mô tả, chấm tròn là RQ3 có kiểm định. Hai cụm xa 0 nhất là G-proj (0.13–0.19) và T-12 (0.39–0.49).

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

### Slide 13. Why BEFORE inflates 12 classes so much
Section: III · Content and method
- Rare classes (PO: 12 rows) are copied many times to match F (444)
- Copies land in both training and test folds
- The model is tested on what it has already seen
Visual: one small box copied many times, arrows into Train and Test.
Notes: Không oversampling, T-12 đạt 0.292–0.563; oversampling đúng cách đạt 0.495–0.597. Khoảng cách tới 0.95–0.99 là do bản sao lọt vào tập test.

### Slide 14. RQ3: do ensembles help?
Section: III · Content and method

| Comparison (G-dup) | Δ | Result |
|---|---|---|
| M5 Voting vs M3 RF | +0.032 | clearly better |
| M6 Stacking vs M3 RF | +0.042 | clearly better |
| M5 / M6 vs LR, SVM, CNB | −0.006 to +0.017 | no clear difference |

- Same pattern under stratified CV
Notes: Phần duy nhất dùng kiểm định vì các mô hình dùng chung split. M1 và M2 cùng là mô hình tuyến tính trên cùng đặc trưng nên lỗi tương quan, gộp lại ít lợi.

### Slide 15. Replication on Dalpiaz et al.
Section: III · Content and method
- BEFORE vs IN-FOLD: +0.034 to +0.081 (same direction, small)
- Unseen dataset (LODO): 0.405–0.511 vs 0.709–0.746 under S
- Drop of 0.21–0.31; rankings barely agree (τ = 0.20)
Visual: two big numbers "+0.03 to +0.08" and "−0.21 to −0.31".
Notes: Dữ liệu nhỏ (327 câu, 4 dataset), kết quả cùng hướng với PROMISE_exp. Tất cả là mô tả.

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

### Slide 17. What is new in this study
Section: IV · Novelty
- First measurement, as far as we found, of how much evaluation choices change FR/NFR scores
- Three practices tested on one fixed pipeline, two datasets, 25 folds per setting
- Paired tests only where test folds match; other comparisons descriptive
- Locked protocol, bit-identical re-run, public code, splits and fold scores
Visual: four icon cards.
Notes: Điểm mới không nằm ở mô hình mà ở cách đo. Nhóm định lượng được mức thổi phồng cho từng thực hành, và làm theo quy trình có thể kiểm chứng lại. Việc tách so sánh có kiểm định và so sánh mô tả (A-009) cũng là một điểm nhóm rút ra cho các nghiên cứu sau.

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

### Slide 19. Thank you! Questions?
Section: V · Conclusion
Code, splits and fold scores: github.com/TaiNguyen66/fr_nfr_ensemble_research
Visual: QR code to the repository.
Notes: Mời thầy cô và các bạn đặt câu hỏi.

---

## Phần 3. Sau khi Canva tạo xong

1. Chèn hình: tải `paper/figures/summary_deltas.png` vào slide 9 và `paper/figures/slide_rq2_t12.png` vào slide 12.
2. Tạo mã QR cho slide 19: Canva → **Apps → QR Code**, nhập link GitHub.
3. Kiểm tra speaker notes; nếu Canva không đưa vào phần *Notes*, chép từ Phần 2.

## Phần 4. Checklist soát lỗi

- [ ] Đủ 19 slide, đúng thứ tự, đúng tiêu đề.
- [ ] Mọi số trong bảng slide 4, 10, 11, 12, 14, 16 khớp từng chữ số với Phần 2.
- [ ] Mỗi slide có nhãn phần (I đến V) đúng như dòng "Section:".
- [ ] Không có chữ "significant", "6/6", "10/10" ở bất kỳ đâu.
- [ ] Chỉ slide 14 có "clearly better" / "no clear difference".
- [ ] Không có câu, trích dẫn hay con số nào Canva tự thêm.
- [ ] Hai hình kết quả đã chèn ở slide 9 và 12.
- [ ] Tên tác giả và link GitHub đúng.
