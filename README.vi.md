# Rò rỉ trong đánh giá làm thổi phồng kết quả phân loại yêu cầu FR/NFR bao nhiêu?

*Đánh giá lại có kiểm soát rò rỉ cho các bộ phân loại đơn và ensemble*

Nguyễn Phát Tài, Hoàng Ánh · Đại học FPT TP.HCM · SWR302 (FA26)

Bản tiếng Anh: [`README.md`](README.md)

Repo này chứa mã nguồn, protocol, chỉ số chia fold và điểm từng fold của nghiên cứu. Nghiên cứu đo xem cách đánh giá làm thay đổi hiệu năng được báo cáo của các bộ phân loại yêu cầu chức năng (FR) và phi chức năng (NFR) đến mức nào.

## Bài báo

Nghiên cứu được viết thành bài báo cho hội nghị ICIIT 2027 (TP.HCM, 4–7/3/2027), đồng thời là báo cáo môn SWR302 (FA26). Mã nguồn LaTeX của bài được lưu riêng, không nằm trong repo này. Repo giữ mọi thứ cần để kiểm tra và chạy lại kết quả: mã nguồn, protocol, chỉ số chia fold, điểm từng fold, kết quả phân tích và các bảng sinh cho bài báo (`results/paper_tables/`).

## Bối cảnh và khoảng trống nghiên cứu

Nhóm lọc tài liệu theo protocol tổng quan (`protocol/review_protocol.md`). Vòng cuối còn 30 bài có PDF, trong đó 21 bài thực nghiệm được giữ lại để tìm khoảng trống. Từ 7 gap sơ bộ (`literature/review/gap_candidates.csv`, `gap_analysis.md`), nhóm chọn:

| Gap | Nội dung | Thành |
|---|---|---|
| G1 | 14/21 bài chia ngẫu nhiên mà không khử trùng; 0/21 bài gom câu trùng vào cùng fold | RQ1(a) |
| G5 | Chỉ 3/21 bài đánh giá trên project chưa thấy | RQ1(b) |
| G2 | 3/6 bài dùng oversampling làm trước khi chia train/test | RQ2 |
| G3 | 4/6 bài ensemble không kiểm định thống kê | RQ3 |
| G4, G6 | Ít bài báo macro-F1; ít bài công bố code/data | Đóng góp phương pháp |
| G7 | Ảnh hưởng của tiền xử lý (đã có Abad et al. 2017) | Bỏ |

## Câu hỏi nghiên cứu

- **RQ1.** Ước lượng hiệu năng và thứ hạng model thay đổi bao nhiêu khi (a) câu trùng và gần trùng luôn nằm cùng fold (G-dup), (b) mọi yêu cầu của một project nằm cùng fold (G-proj), so với stratified CV ngẫu nhiên (S)?
- **RQ2.** Oversampling toàn bộ dữ liệu trước khi chia (BEFORE) thổi phồng ước lượng bao nhiêu so với chỉ oversampling phần train của mỗi fold (IN-FOLD)?
- **RQ3.** Dưới đánh giá có kiểm soát rò rỉ (G-dup), hard voting (M5) và stacking (M6) có tốt hơn các bộ phân loại đơn M1–M4 không?

## Thiết kế

- **Đặc trưng:** TF-IDF unigram và bigram, chỉ fit trên fold train.
- **Model** (scikit-learn, siêu tham số cố định, không tinh chỉnh): M0 dummy, M1 logistic regression, M2 linear SVM, M3 random forest, M4 complement naive Bayes, M5 hard voting (M1–M3), M6 stacking (M1–M3, meta-learner LR).
- **Cách chia:** S, G-dup, G-proj (5-fold) và LODO trên dữ liệu Dalpiaz. Mỗi cấu hình chạy 5 seed, được 25 điểm fold.
- **Oversampling:** NONE, IN-FOLD, BEFORE, với random oversampling (OS-R) và SMOTE (OS-S).
- **Thống kê:** RQ3 dùng corrected repeated k-fold t-test (Nadeau–Bengio) và hiệu chỉnh Holm. "Khác biệt rõ" nghĩa là |Δ| ≥ 0.01 và p sau hiệu chỉnh < 0.05. RQ1, RQ2 và phần tái lập so các test fold khác nhau nên chỉ báo cáo mô tả (hiệu hai trung bình), theo sửa đổi A-009.

## Kết quả chính (macro-F1)

| So sánh | Kết quả |
|---|---|
| RQ2, 12 lớp: BEFORE − IN-FOLD | +0.392 đến +0.491 (BEFORE 0.951–0.994, IN-FOLD 0.495–0.597) |
| RQ2, nhị phân: BEFORE − IN-FOLD | +0.015 đến +0.027 |
| RQ1(b): S − G-proj | 0.134 đến 0.190; thứ hạng model thay đổi (Kendall τ = 0.600) |
| RQ1(a): S − G-dup | dưới 0.01 với mọi model (chỉ có 8 nhóm câu trùng) |
| RQ3: ensemble so với model đơn | chỉ tốt hơn rõ so với random forest (+0.032, +0.042) |
| Tái lập (Dalpiaz et al.) | BEFORE − IN-FOLD +0.034 đến +0.081; S − LODO 0.21 đến 0.31 |

Phân tích lỗi trên 30 dòng phân loại sai (T-bin, G-dup, seed 42) cho thấy ba nhóm lớn nhất là yêu cầu mơ hồ (8), lẫn FR/NFR (7) và động từ chức năng trong NFR (6). Hai người gán nhãn đồng thuận ban đầu 15/30 dòng (κ = 0.391); cả hai đều có dùng AI hỗ trợ khi gán nhãn.

## Dữ liệu

| Bộ dữ liệu | Vai trò | Nguồn | Trong repo |
|---|---|---|---|
| PROMISE_exp (969 yêu cầu, 47 project, 12 lớp) | bộ chính | Lima et al. 2019, bản mirror công khai | không phân phối lại (chưa rõ giấy phép); SHA-256 ở `data/checksums.csv` |
| Dalpiaz et al. 2019 (dronology, leeds, reqview, wasp; 327 yêu cầu) | tái lập | Zenodo, doi:10.5281/zenodo.3309582 | không phân phối lại; tải từ Zenodo |

Chi tiết, ánh xạ nhãn và số dòng mong đợi: [`data/README.md`](data/README.md).

## Cấu trúc repo

```text
protocol/     research_protocol.md (khóa 16/10/2026), amendment_log.md (A-001 đến A-009), review_protocol.md
src/          nạp dữ liệu, chia fold, model, chạy thí nghiệm, thống kê, phân tích, bảng cho bài báo
tests/        unit test (chia fold, kiểm tra rò rỉ, thống kê, phân tích, bảng)
scripts/      chọn tài liệu, bằng chứng từ PDF, đóng băng dữ liệu, hợp nhất nhãn phân tích lỗi
data/         metadata và checksum (không có dữ liệu gốc)
results/
  splits/     chỉ số chia fold cho mọi protocol và seed
  tables/     điểm từng fold, tóm tắt, thống kê (RQ3) và so sánh mô tả
  figures/    forest plot cho RQ3
  paper_tables/  bảng LaTeX và hình tổng hợp dùng trong bài (sinh bởi src/paper_tables.py)
experiments/  experiment_log.csv (mỗi lần chạy một dòng)
literature/   hồ sơ tìm kiếm, quyết định sàng lọc, bộ tài liệu cuối và phân tích gap
research_log.md                 nhật ký làm việc
HUONG_DAN_CHAY_THI_NGHIEM.md    hướng dẫn chạy từng bước
```

## Chạy lại kết quả

Python 3.12 trên Windows (win-amd64); phiên bản thư viện được ghim trong `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# đặt dữ liệu gốc vào data/raw/ (xem data/README.md), rồi:
python -m pytest -q tests                      # 37 test
python -m src.audit_dataset                    # tạo data/processed/
python -m src.run_experiments --plan RQ1       # 525 lần fit
python -m src.run_experiments --plan RQ2       # 1250 lần fit
python -m src.run_experiments --plan D2        # 770 lần fit
python -m src.analyze_results                  # results/tables, results/figures
python -m src.paper_tables                     # results/paper_tables
```

Lần chạy lại toàn bộ ngày 18/10/2026 cho ra đúng từng điểm fold (SHA-256 của mọi `fold_scores_*.csv` trùng khớp). Kết quả mong đợi và thời gian chạy: [`HUONG_DAN_CHAY_THI_NGHIEM.md`](HUONG_DAN_CHAY_THI_NGHIEM.md).

## Không đưa vào repo

Dữ liệu gốc (`data/raw/`), file đã xử lý có chứa câu yêu cầu, dự đoán từng dòng và nhãn phân tích lỗi (`results/predictions/`), PDF toàn văn của các bài đã đọc và log chạy đều bị loại bởi `.gitignore`.

## Giấy phép và trích dẫn

Mã nguồn phát hành theo giấy phép MIT ([`LICENSE`](LICENSE)). Các bộ dữ liệu giữ giấy phép gốc và không được phân phối lại. Thông tin trích dẫn ở [`CITATION.cff`](CITATION.cff).
