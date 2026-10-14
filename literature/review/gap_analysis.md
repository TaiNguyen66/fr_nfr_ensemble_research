# Phân tích khoảng trống (bản đề xuất cho họp chọn gap)

> **Nguồn:** 30 bài vòng cuối (`final_set.csv`), Claude đọc các đoạn liên quan trong toàn văn ngày 12/10 (`claude_verification.csv`).
> **Trạng thái:** ĐÃ CHỐT 14/10 (nhóm chọn "theo đề xuất"). Sau khi hai thành viên kiểm tra, còn **21 bài thực nghiệm** (loại thêm R0043, R0145, R0229, R0813, R0618; R1526 không đếm). Số liệu chính thức: mục 0 bên dưới; protocol: `research_protocol.md` v2.0.
> **Phạm vi đếm:** 26 bài thực nghiệm được giữ. Loại 3 bài: R0014 (review ứng dụng), R0615 (phát hiện câu mơ hồ), R0072 (chỉ xây dataset). R1526 (Allamanis 2019) là bài nền tảng, không đếm.

## 0. Số liệu chính thức sau xác nhận (21 bài)

| Gap | k/N |
|---|---|
| G1 chia ngẫu nhiên không khử trùng | 14/21; 0/21 nhóm câu trùng |
| G2 oversampling trước khi chia | 3 trong 6 bài có oversampling |
| G3 ensemble không kiểm định | 4/6 |
| G4 báo macro-F1 | 1/21 |
| G5 đánh giá theo project/domain | 3/21 (+ NoRBERT một phần) |
| G6 công bố code/data | 5/21 |

## 1. Bằng chứng theo từng gap (bản đọc trước, 26 bài)

| Gap | Bằng chứng (k/N trên 26 bài) | Mức |
|---|---|---|
| **G1 – Câu trùng nằm ở cả train và test** | **15/26** chia ngẫu nhiên, không khử trùng; **0/26** nhóm câu trùng khi chia; 5/26 không nêu cách chia | Mạnh |
| **G2 – Oversampling trước khi chia** | 7/26 dùng oversampling: **3 làm trước khi chia** (R0187, R0538, R0632), 3 làm đúng (R0181, R0517, R0719), 1 không rõ (R0618) | Mạnh, chưa ai đo |
| **G3 – Ensemble không kiểm định** | 6 bài ensemble: **4/6 không kiểm định**; 2 bài có kiểm định (R0187, R0617) vẫn chia ngẫu nhiên không khử trùng | Mạnh |
| G4 – Báo cáo không so được | Macro-F1: **1/26**; weighted: 4/26; chỉ accuracy: 5/26 | Đóng góp phương pháp |
| G5 – Tổng quát hóa theo project | **4/26** đánh giá theo project / domain | Trung bình |
| G6 – Tái lập | **5/26** công bố code/data | Đóng góp phụ |
| G7 – Tiền xử lý | 1/26 tách riêng ảnh hưởng (Abad 2017 đã làm) | Yếu → bỏ |

**Quan sát đáng chú ý:** hai bài báo accuracy cao nhất cả bộ (R0632: 98,79%; R0538: 99%) đều có dấu hiệu oversampling *trước* khi chia. Ngược lại, các bài đánh giá theo project báo kết quả thấp hơn rõ (R1341: F1 0,62). Điều này khớp với giả thuyết rằng cách đánh giá đang thổi phồng hiệu năng. Allamanis (2019) đã chứng minh hiện tượng tương tự ở bài toán code (thổi phồng tới 100%), nhưng **chưa bài nào lượng hóa cho phân loại yêu cầu FR/NFR**.

## 2. Đề xuất chọn gap

- **Gap chính: rò rỉ dữ liệu trong đánh giá phân loại FR/NFR** (gộp G1 + G2). Bằng chứng mạnh nhất, khả thi (chỉ cần PROMISE_exp và đổi cách chia / thứ tự oversampling), đúng tên đề tài "leakage-aware", và có đóng góp mới (đo mức thổi phồng).
- **Gap phụ 1: ensemble dưới đánh giá có kiểm soát rò rỉ** (G3). Giữ RQ1 của thiết kế v1.1, thêm kiểm định.
- **Gap phụ 2: tổng quát hóa theo project** (G5). Chỉ giữ nếu audit thấy PROMISE_exp có đủ project (quy tắc khả thi G-proj trong protocol v1.1 §8).
- **Không thành RQ:** G4, G6 (làm thành đóng góp phương pháp: báo macro-F1 + theo lớp, công bố repo và dataset freeze).
- **Bỏ:** G7 tiền xử lý (RQ2 của v1.1). Bỏ giúp giảm 2/3 số cấu hình thí nghiệm, dành thời gian cho G2.

Tất cả đều qua bộ lọc khả thi (`review_protocol.md` §8): dữ liệu công khai, chạy CPU, code ≤ 5 ngày, metric chuẩn, không cần LLM / GPU / gán nhãn mới.

## 3. Đề xuất RQ cho protocol v2.0

| RQ | Câu hỏi | Gap | Thay đổi so với v1.1 |
|---|---|---|---|
| **RQ1** | Ước lượng hiệu năng và thứ hạng model thay đổi bao nhiêu khi câu trùng / gần trùng luôn nằm cùng fold (G-dup), và khi chia theo project (G-proj), so với CV phân tầng ngẫu nhiên? | G1, G5 | Là RQ3 cũ, đưa lên thành câu hỏi chính |
| **RQ2** | Oversampling trên toàn bộ dữ liệu *trước* khi chia làm thổi phồng ước lượng bao nhiêu so với oversampling *trong* tập train của từng fold? | G2 | **Mới**, thay RQ2 tiền xử lý |
| **RQ3** | Dưới đánh giá có kiểm soát rò rỉ, Voting / Stacking có tốt hơn LR / SVM / RF / NB một cách có ý nghĩa thống kê không (corrected t-test + Holm)? | G3 | Là RQ1 cũ, chạy trên protocol có kiểm soát rò rỉ |

**Thiết kế RQ2 (gợi ý, chốt trong protocol v2.0):** cùng model và cùng fold, hai điều kiện: (a) random oversampling / SMOTE áp dụng lên toàn bộ dữ liệu rồi mới chia (tái hiện cách làm của R0632, R0538, R0187); (b) oversampling chỉ trên tập train của từng fold. So Δ macro-F1 giữa (a) và (b) theo quy tắc kết luận §10. Nhiệm vụ: binary FR/NFR và multi-class 12 lớp (multi-class mất cân bằng nặng nên dễ thấy hiệu ứng). Chi phí thêm thấp: chỉ thêm một bước trong pipeline.

**Tiền xử lý:** cố định P0 (tối thiểu) cho mọi thí nghiệm; ghi trong Threats to Validity.

## 4. Hạn chế của bản phân tích này

- Claude đọc các đoạn liên quan, không đọc toàn văn từng câu. Các ô có độ chắc chắn "thấp" / "trung bình" cần người kiểm tra trước khi số liệu thành chính thức. Ưu tiên kiểm tra: R0187, R0538, R0618 (thứ tự oversampling); R0043, R0118, R0145, R0229, R0813 (không nêu cách chia).
- Bộ 30 bài chỉ gồm bài có bản open access tải được tự động (A-004). Bài quan trọng không có bản mở (Canedo & Mendes 2020, Kurtanović & Maalej 2017, ESEM 2025 Voting/Stacking) có thể được trích dẫn từ abstract cho bối cảnh, nhưng không đưa vào số đếm.
