# Literature Review Protocol

| Trường | Giá trị |
|---|---|
| Phiên bản | 1.0 (2026-10-12) |
| Trạng thái | LOCKED khi hai thành viên đồng ý (amendment A-003). Đổi tiêu chí sau đó = amendment mới |
| Phạm vi | Giai đoạn 1–3 của kế hoạch (12/10 → 22/10/2026). Thiết kế thí nghiệm nằm ở `research_protocol.md` |
| Loại review | **Targeted literature review** có ghi nhật ký tìm kiếm và sàng lọc nhiều vòng. Không gọi là SLR/PRISMA đầy đủ |

## 1. Mục tiêu

Từ tài liệu đã công bố về phân loại yêu cầu FR/NFR, tìm **khoảng trống (gap) có bằng chứng** mà nhóm làm được trong nguồn lực hiện có. Từ gap đó chốt câu hỏi nghiên cứu và thiết kế thí nghiệm (`research_protocol.md` v2.0).

## 2. Câu hỏi của review (LRQ)

| Mã | Câu hỏi | Dùng để |
|---|---|---|
| LRQ1 | Những kỹ thuật nào (ML cổ điển, ensemble, deep learning, LLM) đã được dùng cho phân loại FR/NFR, trên dataset nào, kết quả ra sao? | Bối cảnh, baseline |
| LRQ2 | Các nghiên cứu **đánh giá** thế nào: cách chia dữ liệu, kiểm soát trùng lặp / leakage, cross-project, loại F1, kiểm định thống kê? | Gap về phương pháp đánh giá |
| LRQ3 | Bằng chứng về **ensemble** so với model đơn lẻ có nhất quán và so sánh công bằng không? | Gap về RQ1 ứng viên |
| LRQ4 | Tiền xử lý và biểu diễn văn bản ảnh hưởng thế nào, có được kiểm tra riêng không? | Gap về RQ2 ứng viên |
| LRQ5 | Nghiên cứu có tái lập được không (dataset/version, code, tham số)? | Gap về tái lập |

RQ ứng viên hiện tại (`research_protocol.md` v1.1 §3: ensemble, tiền xử lý, leakage/project) là **giả thuyết khởi đầu**. Review có thể xác nhận, thu hẹp hoặc thay chúng.

## 3. Nguồn và chiến lược tìm kiếm

- **Công cụ:** `tools/frnfr-metadata-fetcher` v3.0.0-frnfr. Nguồn OpenAlex, Semantic Scholar, arXiv. Tìm trên title + abstract, năm 2017–2026.
- **Chuỗi:** Q1, Q1b, Q2, Q3, Q4 (core), Q5 (tiền xử lý), T1 (leakage), T2 (thống kê). Chuỗi đầy đủ: `literature/search/search-log.md`.
- **Đã chạy:** 2026-10-09. 1.276 bản ghi duy nhất. Known-paper check 7/7 HIT (`literature/search/rq-check.md`).
- **Bổ sung tay** (ghi vào `search-log.md`): tra Google Scholar / IEEE Xplore / ACM DL cho chuỗi Q1–Q2, và snowballing ngược/xuôi từ 3–5 bài cốt lõi sau R3 nếu thiếu bài nhóm ensemble hoặc đánh giá.
- **Thêm tay:** 5 paper nền ngoài khung năm/chuỗi (S01–S05).

## 4. Vòng R0 – Lọc tự động (đã xong)

Luật từ khóa của công cụ gắn INCLUDE / BACKGROUND / UNSURE / EXCLUDE. **R0 không loại bài nào khỏi R1** ngoài nhóm EXCLUDE rõ ràng; kết quả R0 chỉ để xếp thứ tự và gợi ý.

Đưa vào R1: mọi bản ghi từ stream core có gợi ý INCLUDE / UNSURE / BACKGROUND (466), 40 bài nền tảng T1/T2 nhiều trích dẫn nhất có tiêu đề về leakage / cross-validation / so sánh classifier, và 5 bài thêm tay. Tổng **511**.

## 5. Vòng R1 – Tiêu đề + tóm tắt (12/10 → 14/10)

**Tiêu chí giữ (cả hai đúng):**
- IC1: bài tự động phân loại yêu cầu phần mềm (FR/NFR, loại NFR hoặc loại yêu cầu) bằng NLP/ML; **hoặc** là bài nền tảng dùng được cho Related Work / phương pháp (survey NLP4RE, leakage, cross-validation, so sánh classifier).
- IC2: có đánh giá định lượng (với bài nghiên cứu thực nghiệm).

**Tiêu chí loại (mã):** EC-S ngoài phạm vi · EC-T sai nhiệm vụ / loại văn bản (app review, issue report, văn bản pháp lý) hoặc không dùng NLP/ML · EC-E không có đánh giá định lượng · EC-D trùng · EC-Y trước 2017 (trừ paper nền) hoặc không phải tiếng Anh · EC-G không phải bài nghiên cứu.

**Cách làm:**
- Mỗi người sàng lọc phần được phân công (Phat Tai ~60%, Hoang Anh ~40%).
- **55 bài (~10%) cả hai cùng sàng lọc độc lập.** Tính Cohen's κ trên KEEP+MAYBE vs DROP. κ < 0,6 → hai người đọc lại tiêu chí, thống nhất cách hiểu, rà lại phần của mình.
- Không chắc → MAYBE (sang R2). Ưu tiên giữ nhầm hơn loại nhầm ở vòng này.

**Đầu ra dự kiến:** 80–120 bài KEEP/MAYBE.

## 6. Vòng R2 – Đủ điều kiện (15/10 → 16/10)

Mở toàn văn, đọc lướt (~5 phút/bài): abstract, phần method/evaluation, bảng kết quả.

| Mã | Kiểm tra | Bắt buộc |
|---|---|:---:|
| E1 | Dataset có tên và truy cập được | |
| E2 | Có kết quả cho FR/NFR hoặc loại yêu cầu (không chỉ app review / issue) | ✔ |
| E3 | Kỹ thuật (ML cổ điển / ensemble / DL / LLM) | ghi lại |
| E4 | Mô tả cách chia dữ liệu / đánh giá | ✔ |
| E5 | Có toàn văn | ✔ |
| D1–D3 | Liên quan: D1 ensemble · D2 tiền xử lý/biểu diễn · D3 đánh giá/leakage/tổng quát hóa | ghi lại |

Bài nền tảng (survey, leakage, thống kê) chỉ cần E5.

**Chọn sang R3 (30–40 bài):** đủ E2+E4+E5; ưu tiên bài có D1 hoặc D3, venue bình duyệt, dataset công khai; đảm bảo có đủ 4 nhóm.

## 7. Vòng R3 – Toàn văn, trích xuất, chất lượng (17/10 → 19/10)

Đọc toàn văn, điền tab `R3_ToanVan_QA`: dataset (+version), nhiệm vụ, biểu diễn, model, tiền xử lý, **cách chia dữ liệu**, **kiểm soát trùng lặp/leakage**, metric, **loại F1**, kết quả tốt nhất kèm điều kiện, kiểm định thống kê, code/data công khai, so được với mình không, hạn chế.

**Chất lượng (QA), mỗi tiêu chí 0/1/2:**
- Q1: mục tiêu và câu hỏi rõ ràng.
- Q2: dataset mô tả đủ và truy cập được.
- Q3: đánh giá chặt chẽ (cách chia nêu rõ, không rò rỉ hiển nhiên, baseline hợp lý).
- Q4: kết quả đủ (metric phù hợp, có độ biến thiên hoặc nhiều lần chạy).
- Q5: nêu hạn chế và có thể tái lập (code/data/tham số).

Tổng ≥ 6 → tổng hợp chính. < 6 → giữ nhưng gắn LOW-CONFIDENCE.

**Bộ bài chốt:** 15–20 bài, gồm ≥ 12 bài thực nghiệm và 3–5 bài nền tảng; mỗi nhóm có ≥ 3 bài:
- CORE-ML: phân loại FR/NFR bằng ML/NLP.
- CORE-ENSEMBLE: ensemble cho phân loại yêu cầu.
- EVALUATION: dataset / cách chia / cross-project / leakage.
- BACKGROUND: survey, leakage, thống kê.

Thiếu nhóm nào → snowballing từ bài cốt lõi của nhóm đó (tối đa nửa ngày).

## 8. Tổng hợp và tìm khoảng trống (20/10 → 22/10)

1. **Bảng so sánh** từ R3: dataset × kỹ thuật × cách chia × loại F1 × kết quả × QA. Đếm theo từng cột (ví dụ: "k/N bài dùng 10-fold ngẫu nhiên không xử lý trùng lặp").
2. **Liệt kê gap** vào tab `GD3_Gap`, mỗi gap phải có **bằng chứng đếm được** (ID bài, k/N). Loại gap: phương pháp đánh giá · so sánh công bằng · dữ liệu · tái lập · kỹ thuật.
3. **Lọc theo khả thi.** Gap chỉ được chọn khi đạt **tất cả**:
   - Dữ liệu công khai, tải và kiểm tra được trước 22/10.
   - Chạy được trên CPU laptop; toàn bộ thí nghiệm < 1 ngày tính toán.
   - Code + test làm xong trong ≤ 5 ngày cho 2 người.
   - Đo được bằng metric chuẩn, có quy tắc kết luận định trước.
   - Không cần LLM trả phí, GPU, khảo sát người dùng hay gán nhãn mới quy mô lớn.
4. **Chọn 1 gap chính + tối đa 2 gap phụ** → viết RQ chính thức → `research_protocol.md` v2.0 (khóa trước khi chạy).
5. **Phương án mặc định:** nếu không gap nào đạt bước 3 hoặc bằng chứng yếu, dùng RQ ứng viên v1.1 (vẫn khả thi), ghi rõ lý do.

**Đầu ra GĐ3:** bảng so sánh, bảng gap (đã chọn), bản nháp Related Work 1,5–2 trang, `research_protocol.md` v2.0.

## 9. Lưu trữ và truy vết

- Workbook làm việc: Google Sheet trên Drive nhóm (tạo từ `literature/review/NCKH_FRNFR_Literature.xlsx` bằng `scripts/build_screening_workbook.py`).
- Cuối mỗi vòng: xuất Sheet ra `.xlsx`, lưu vào `literature/review/` với hậu tố vòng (`…_R1.xlsx`, `…_R2.xlsx`, `…_R3.xlsx`) và commit. Số liệu trong bài báo (số bài mỗi vòng, κ) lấy từ các file này.
- PDF toàn văn: Zotero hoặc Drive `01_Tai_lieu_tham_khao/`. Không commit PDF lên GitHub.
- Báo cáo trong bài: một sơ đồ luồng sàng lọc (số bài sau R0 → R1 → R2 → R3) và bảng tiêu chí.
