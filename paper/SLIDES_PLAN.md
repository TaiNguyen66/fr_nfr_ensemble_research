# Kế hoạch slide (Canva, tiếng Anh, 15–20 phút, 17 slide + Q&A)

Nội dung chữ trên slide viết bằng tiếng Anh, lấy số từ `fact_sheet.md`. Phần "Nói" là gợi ý lời thuyết trình.
Người trình bày là **đề xuất**, Phat Tai quyết định. Thời lượng mục tiêu khoảng 18 phút.

## Cách làm trên Canva

1. Canva → *Presentations (16:9)* → chọn template tối giản (gợi ý từ khóa: "minimal research", "academic"), chữ tối trên nền sáng, tối đa 2 màu nhấn.
2. Mỗi slide tối đa khoảng 30 từ chữ trên màn hình; phần chi tiết đặt trong *Notes*.
3. Hình: tải lên từ `paper/figures/`: `summary_deltas.png`, `slide_rq2_t12.png`, và các forest plot trong `results/figures/delta_*.png` khi cần.
4. Sơ đồ thiết kế (slide 7) vẽ lại bằng shape của Canva theo `figures/design.tex` (hai hàng BEFORE / IN-FOLD, ba ô S / G-dup / G-proj), hoặc chụp từ PDF Overleaf.
5. Không dùng Magic Write / AI của Canva để sinh nội dung hay con số.
6. Share Canva cho Hoang Anh quyền *Can edit*; xuất PDF dự phòng trước buổi trình bày.

## Dàn ý

| # | Tiêu đề (EN) | Nội dung trên slide | Hình / bảng | Nói (ý chính) | Người | Phút |
|---|---|---|---|---|---|---|
| 1 | How Much Does Evaluation Leakage Inflate FR/NFR Requirements Classification? | Tên, tác giả, môn SWR302, ngày | — | Giới thiệu nhóm và đề tài | Phat Tai | 0.5 |
| 2 | Why FR/NFR classification? | FR vs NFR, 1 ví dụ mỗi loại; automating RE triage | 2 câu ví dụ từ PROMISE_exp | Bài toán và vì sao cần tự động | Phat Tai | 1 |
| 3 | Reported results look almost perfect | "98.79% accuracy", "99%" (2 nghiên cứu đã review); câu hỏi: are we measuring the model or the evaluation? | Số lớn | Gợi tò mò, không nói các bài đó sai | Phat Tai | 1 |
| 4 | What we found in 21 studies | 14/21 random split, 0/21 group duplicates; 3/6 oversample before split; 4/6 untested ensemble claims; 1/21 macro-F1; 3/21 unseen-project evaluation | Bảng nhỏ hoặc icon | Bằng chứng từ review → gap | Phat Tai | 1.5 |
| 5 | Research questions | RQ1 duplicates / projects; RQ2 oversampling order; RQ3 ensembles | 3 thẻ | Mỗi RQ một câu | Phat Tai | 1 |
| 6 | Data | PROMISE_exp 969 req., 47 projects, 12 classes, 8 duplicate groups; Dalpiaz 327 req., 4 projects (replication) | Phân bố lớp (tùy chọn) | Dataset và cách gán nhãn | Hoang Anh | 1 |
| 7 | Evaluation design | S / G-dup / G-proj; BEFORE vs IN-FOLD | Sơ đồ (vẽ lại từ `design.tex`) | Giải thích vì sao BEFORE làm rò rỉ | Hoang Anh | 1.5 |
| 8 | Models and pipeline | TF-IDF in-fold; M0 dummy, M1 LR, M2 SVM, M3 RF, M4 CNB, M5 voting, M6 stacking; no tuning | Sơ đồ pipeline đơn giản | Cố định trước, không tinh chỉnh | Hoang Anh | 1 |
| 9 | Fair comparison | 5 seeds × 5 folds = 25 paired scores; corrected t-test + Holm; "clear" = \|Δ\| ≥ 0.01 and p < 0.05; protocol locked before running | — | Vì sao cần kiểm định đã hiệu chỉnh | Hoang Anh | 1 |
| 10 | Overview of results | 0/6, 6/6, 0/10, 10/10, 2/8, 0/10 | `summary_deltas.png` | Hình toàn cảnh: hai cụm nổi bật | Phat Tai | 1 |
| 11 | RQ1: duplicates and projects | Duplicates: no clear difference (only 8 groups). Unseen projects: −0.13 to −0.19 macro-F1, rankings change (τ = 0.60) | `delta_RQ1-proj.png` hoặc bảng RQ1 rút gọn | Kết quả âm vẫn là kết quả; G-proj không gọi là leakage | Phat Tai | 1.5 |
| 12 | RQ2: binary task | BEFORE − IN-FOLD +0.015 to +0.027, no clear difference | `delta_RQ2-bin.png` | Mất cân bằng nhẹ thì ảnh hưởng nhỏ | Phat Tai | 1 |
| 13 | RQ2: 12 classes, the main finding | IN-FOLD ≈ 0.50–0.60 → BEFORE ≈ 0.95–0.99 (+0.39 to +0.49, 10/10 clear) | `slide_rq2_t12.png` | Kết quả chính: lớp hiếm bị nhân bản nên test "đã thấy" | Phat Tai | 2 |
| 14 | RQ3: do ensembles help? | Better than RF only (+0.03/+0.04); no clear difference vs LR, SVM, CNB | `delta_RQ3-Gdup.png` | Mô hình nền tương quan nên ensemble không vượt mô hình tuyến tính tốt nhất | Hoang Anh | 1 |
| 15 | Replication on Dalpiaz et al. | Same direction for BEFORE (+0.03 to +0.08, not clear); unseen dataset −0.21 to −0.31 (descriptive) | Bảng Dalpiaz rút gọn | Dataset nhỏ nên kiểm định yếu hơn | Hoang Anh | 1 |
| 16 | Threats and lessons | 1 main benchmark; fixed hyperparameters; classical models; folds paired by index in BEFORE | — | Trung thực về giới hạn | Hoang Anh | 1 |
| 17 | Recommendations and conclusion | 1) oversample in-fold only; 2) group duplicates; 3) report unseen-project results; 4) macro-F1 + corrected tests; 5) publish code and splits. Repo link / QR | QR tới GitHub | Thông điệp chính | Phat Tai | 1 |
| — | Q&A / Thank you | — | — | — | Cả hai | — |

## Câu hỏi có thể gặp (chuẩn bị trước)

- *Vì sao không dùng BERT/LLM?* Nằm ngoài phạm vi theo thiết kế: đây là nghiên cứu về cách đánh giá, nên cần pipeline rẻ và cố định. Hướng tương lai là chạy cùng protocol cho transformer.
- *BEFORE và IN-FOLD không cùng tập test thì so sánh có công bằng không?* Hai điều kiện được ghép theo (seed, fold). Đây chính là cách các nghiên cứu làm BEFORE báo cáo kết quả, và điều này đã ghi trong Threats.
- *Vì sao RQ1a không có hiệu ứng?* PROMISE_exp chỉ có 8 nhóm trùng (16/969 câu). Đây là kết quả âm trên dataset này, không có nghĩa là trùng lặp không bao giờ quan trọng.
- *Corrected t-test là gì?* Các fold dùng chung dữ liệu train nên phương sai bị đánh giá thấp. Nadeau & Bengio hiệu chỉnh bằng tỉ lệ n_test/n_train.
