# Amendment log

Mọi thay đổi RQ, dataset, split, model, metric hoặc quy tắc kết luận sau khi protocol được khóa đều ghi ở đây **trước khi** chạy lại. Không xóa hay sửa mục cũ; mục mới tham chiếu mục cũ nếu cần.

| ID | Ngày | Người đề xuất | Thay đổi | Lý do | Tác động lên kết quả đã có | Hai TV đồng ý |
|---|---|---|---|---|---|---|
| A-001 | 2026-10-08 | Nhóm (góp ý review kế hoạch) | Protocol v1 → v1.1 (xem chi tiết dưới) | v1 mâu thuẫn với kế hoạch và thiếu các tham số phải khóa trước | Không có (chưa chạy model nào) | ☑ A ☑ B (2026-10-09) |
| A-002 | 2026-10-09 | Phat Tai | Chỉ sửa trình bày (editorial): ghi tên thành viên vào bảng ký tên §14 của protocol (TV A = Hoang Anh, TV B = Phat Tai) và README. Không đổi RQ, dữ liệu, model, split, metric hay quy tắc kết luận | Đồng bộ với tài liệu kế hoạch trên Drive | Không có | ☑ Hoang Anh ☑ Phat Tai (2026-10-09) |
| A-003 | 2026-10-12 | Phat Tai | Đổi thứ tự nghiên cứu: review tài liệu nhiều vòng (`review_protocol.md`) → tìm gap → chốt RQ và thiết kế thí nghiệm `research_protocol.md` **v2.0 ngày 22/10**. v1.1 thành thiết kế ứng viên / phương án mặc định | RQ nên xuất phát từ gap có bằng chứng trong tài liệu, không đặt trước | Không có (chưa chạy model nào). Lịch: thí nghiệm dời sang 23/10–05/11 | ☐ Hoang Anh ☑ Phat Tai |
| A-004 | 2026-10-12 | Phat Tai | Đẩy nhanh sàng lọc: thay R1/R2 làm tay bằng lọc tự động L1–L5 (`scripts/select_final_papers.py`): loại UNSURE/EXCLUDE, thiếu abstract, không bình duyệt, không đúng phân loại FR/NFR, và bài **không tải được PDF ngay lần đầu** (bị chặn / xác nhận bot / không có bản open access). Vòng cuối 30 bài (luân phiên nhóm, dừng khi đủ 30); người duyệt loại thêm R0132, R0117, R0418. Chốt gap + protocol v2.0 sớm hơn: **17/10** | Rút thời gian sàng lọc để có thêm thời gian thí nghiệm | Không có kết quả thí nghiệm. **Hạn chế cần nêu trong bài:** bỏ sót bài không có bản open access (gồm Canedo & Mendes 2020, Kurtanović & Maalej 2017, ESEM 2025 Voting/Stacking, Kapoor & Narayanan 2023) | ☐ Hoang Anh ☑ Phat Tai |
| A-005 | 2026-10-14 | Phat Tai | Protocol **v2.0** từ kết quả review (21 bài đã xác nhận): RQ1 = câu trùng / project cùng fold (G1, G5); RQ2 mới = oversampling trước vs trong fold (G2); RQ3 = ensemble dưới đánh giá có kiểm soát rò rỉ + kiểm định (G3). **Bỏ RQ tiền xử lý** (G7 yếu, Abad 2017 đã làm), cố định P0. Thêm nhiệm vụ 12 lớp cho RQ2; thêm `imbalanced-learn`; RQ3 dùng G-dup làm protocol chính | Gap chính có bằng chứng: 14/21 chia ngẫu nhiên không khử trùng, 0/21 nhóm câu trùng, 3/6 oversampling trước khi chia, 4/6 ensemble không kiểm định | Không có (chưa chạy model nào) | ☐ Hoang Anh ☑ Phat Tai |
| A-006 | 2026-10-14 | Phat Tai | (1) Dataset: dùng bản mirror PROMISE_exp trên GitHub (Lima et al. 2019; SHA-256 `7475c290…`), license UNKNOWN nên không đưa file thô lên GitHub. (2) Audit nhanh: chỉ 3 nhóm câu trùng chính xác (6 dòng) → giữ RQ1(a), báo kết quả âm nếu hiệu ứng nhỏ (đúng protocol §10). (3) Duyệt 14 cặp gần trùng: Phat Tai đề xuất SAME/DIFFERENT, **một** thành viên xác nhận (thay vì hai người duyệt độc lập như §4.2) | Không tìm thấy bản phát hành gốc; số cặp gần trùng ít (14) nên một người duyệt là đủ | Không có (chưa chạy model nào) | ☐ Hoang Anh ☑ Phat Tai |

## A-001 chi tiết (v1 → v1.1)

1. Lịch rút về **4 tuần** (09/10 → 05/11/2026).
2. RQ3 tách thành (a) group theo duplicate/near-duplicate và (b) **group theo `ProjectID`** (protocol G-proj). Thêm Kendall's τ cho thay đổi xếp hạng.
3. Repeated CV: 5 seed × 5 fold là **core** cho cả 3 protocol (v1 ghi repeated nhưng kế hoạch để P1; chi phí tính toán nhỏ nên giữ core).
4. Feature core chỉ unigram+bigram; unigram-only thành tùy chọn (v1 để cả hai là core).
5. Thêm M0 `DummyClassifier` (mức sàn) và M4 `ComplementNB` (baseline phổ biến trong tài liệu). Voting/Stacking vẫn dùng M1–M3.
6. Stacking tự cài đặt với inner CV cùng loại splitter với outer protocol; bỏ M6 nếu unit test chưa qua cuối tuần 2.
7. Khóa trước: `KEEP_WORDS`, quy tắc P0/P1/P2 (lemmatization có POS), tham số TF-IDF (`min_df=2`, `sublinear_tf=True`), hyperparameter model, quy tắc canonical text và ngưỡng near-duplicate 0.90, xử lý nhãn xung đột (giữ nguyên nhãn gốc).
8. Thêm quy tắc kết luận: Δ Macro-F1 ≥ 0.01 và corrected repeated k-fold t-test (Nadeau & Bengio) có Holm.
9. Error analysis cố định cách lấy mẫu (30 lỗi, M2 và M5, P0/S/seed 42).
10. Review lần 2 (08/10): S là protocol chính cho RQ1/RQ2 (G-dup là độ nhạy); định nghĩa rõ các comparison family cho Holm; RQ3(b) gọi là project-level generalization, không gọi là leakage; quy tắc khả thi G-proj (mỗi test fold ≥ 2 project, ≥ 10% dòng, ≥ 20% mỗi lớp; không đạt thì thử 3 fold, vẫn không đạt thì bỏ); Macro-F1 tính theo fold rồi lấy trung bình; error analysis = 30 lỗi tổng (15 M2 + 15 M5).
11. Đổi tên file `research_protocol_v1.md` → `research_protocol.md`; phiên bản ghi trong file, lịch sử nằm trong Git.
