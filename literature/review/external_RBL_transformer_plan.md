# Tài liệu ngoài: kế hoạch RBL "Transformer đơn trên PROMISE_exp"

File: `literature/pdf/RBL_transformer_PROMISE_exp_plan.pdf` (kế hoạch nội bộ ngày 2026-10-14, nguồn số liệu: repo ReqLens; gitignored).
**Không phải bài đã bình duyệt, không nằm trong 21 bài của gap_analysis.** Không dùng để thay đổi protocol (đã LOCKED, A-008).

## Nó là gì
So sánh BERT, RoBERTa, ELECTRA, ModernBERT trên PROMISE_exp (969 mẫu, 12 lớp), một lần chia stratified 70/15/15 (test 146), augmentation trên train.

## Dùng được vào đâu
- Intro/Discussion (động cơ cho RQ2): Bảng 6 báo Macro-F1 0.83–0.86 khi augmentation trước khi chia (test 349 mẫu) so với 0.71–0.72 khi test sạch (146 mẫu).
- Threats/Discussion: thiết kế đó không xử lý câu trùng, không lặp seed, không kiểm định; lớp thiểu số chỉ có 2–3 mẫu test.

## Hạn chế khi trích (bắt buộc nêu)
- Số liệu lấy từ notebook, chưa bình duyệt, chưa kiểm lại.
- Chênh lệch gộp hai yếu tố: kích thước/thành phần test (349 vs 146) và rò rỉ mẫu nhân tạo; không tách được hiệu ứng rò rỉ.
- Khác mô hình (Transformer) và khác cách chia với nghiên cứu này → theo protocol §10 không tuyên bố hơn/kém so với các số này.

## Đoạn nháp (EN, cho Intro hoặc Related Work; chỉnh lại trước khi dùng)
> Evidence that pre-split augmentation inflates scores also appears outside the studies we reviewed. In an internal replication on PROMISE_exp with transformer encoders, oversampling the minority classes before the train/test split enlarged the test set from 146 to 349 requirements and raised Macro-F1 from about 0.71–0.72 to 0.83–0.86 (unreviewed notebook results; the figures conflate test-set composition with leakage of synthetic variants). We therefore measure the effect directly: the same classifiers and folds are evaluated with oversampling applied before versus inside each training fold, over repeated cross-validation with duplicate-aware grouping and corrected significance tests.

> Cite as personal communication / project report [dataset+code: ReqLens repo], not as a published study.
