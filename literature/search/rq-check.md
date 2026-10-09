# RQ Check – phat-tai

> **Đề tài:** *A Reproducible and Leakage-Aware Evaluation of Ensemble Learning for FR/NFR Requirements Classification*  
> **Người chạy:** phat-tai | **Cập nhật:** 2026-10-09 | **Protocol:** `fr_nfr_ensemble_research/protocol/research_protocol.md` research_protocol.md v1.1 (2026-10-09)  
> **Cách sinh:** tính tự động từ `01_all_records.csv`, `review-decisions.csv` và `search-runs/*.json` bằng `tools/frnfr-metadata-fetcher/cli.mjs screen` (v3.0.0-frnfr).
> Đây là **targeted literature review** có ghi nhật ký tìm kiếm, không phải SLR/PRISMA đầy đủ.

## 1. Câu hỏi nghiên cứu (protocol §3)

- **RQ1** Individual (LR, Linear SVM, RF, Complement NB) vs ensemble (Hard Voting, Stacking) trong phân loại FR/NFR nhị phân.
- **RQ2** Ảnh hưởng của tiền xử lý P0 / P1 (bỏ stopword) / P2 (+ lemmatization).
- **RQ3** Ước lượng và thứ hạng thay đổi thế nào khi (a) câu trùng/gần trùng cùng fold, (b) cùng project cùng fold.

## 2. Bản đồ bằng chứng (0 study core đã đọc toàn văn)

| ID | Study | Nhóm | Split | F1 type | So được? | Kết quả chính (người đọc tóm tắt) |
|---|---|---|---|---|---|---|
| — | _Chưa có study core_ | | | | | |

## 3. Known-paper check

Kiểm tra trên **dữ liệu export thực tế** trong `01_all_records.csv` (khớp tiêu đề chuẩn hoá, gồm cả bản trùng).
MISS ở paper nền thì thêm stream hẹp hơn (Q1b…) hoặc lấy qua snowballing, và ghi vào `search-log.md`.

| Paper | Vai trò | Stream kỳ vọng | Kết quả | Stream đã bắt được | Snowballing | ID |
|---|---|---|---|---|---|---|
| Canedo & Mendes 2020 | Baseline TF-IDF + LR trên PROMISE_exp | Q1 / Q3 / Q5 | HIT | Q1b, Q2, Q3, Q5 | — | `R0483`, `R0543`, `R0782`, `R1073`, `R1160`, `R1172`, `R1346`, `R1435`, `R1520` |
| Kurtanović & Maalej 2017 | Baseline FR/NFR kinh điển | Q1 | HIT | Q1, Q1b | — | `R0001`, `R0250`, `R0539`, `R0698` |
| Abad et al. 2017 | Tiền xử lý | Q1 / Q5 | HIT | Q1, Q1b, Q3 | — | `R0125`, `R0208`, `R0405`, `R0491`, `R0682`, `R0883`, `R1174`, `R1278`, `R1353` |
| Dalpiaz et al. 2019 | PROMISE gán nhãn lại | Q1b / Q3 | HIT | Q1b | — | `R0484` |
| Hey et al. 2020 (NoRBERT) | Đánh giá cross-project | Q1 / Q3 / Q4 | HIT | Q1, Q1b, Q3, Q4 | — | `R0181`, `R0496`, `R1171`, `R1326`, `R1358`, `R1406` |
| ESEM 2025 Voting/Stacking | Gần nhất với RQ1 | Q2 | HIT | Q1b, Q2, Q3 | — | `R0611`, `R0857`, `R1069`, `R1145`, `R1200`, `R1317` |
| Kapoor & Narayanan 2023 | Khung lý thuyết leakage | T1 | HIT | T1 | — | `R1529`, `R1631` |

## 4. Khoảng trống (TẠM THỜI, chỉ trên các study đã đọc toàn văn)

- RQ1: study về **ensemble** cho phân loại yêu cầu: 0.
- Dùng **PROMISE / PROMISE_exp**: 0 / 0.
- Chia dữ liệu **ngẫu nhiên / k-fold thường**: 0 / 0; **cross-project / theo project**: 0.
- RQ3: xử lý **duplicate / leakage** khi chia dữ liệu: 0 / 0.
- Báo **macro-F1**: 0; **weighted-F1**: 0 (khác loại F1 thì không so trực tiếp).
- Có **kiểm định thống kê** khi so model: 0 / 0.
- Kết quả **so được trực tiếp** với protocol của mình (comparable = Yes): 0 / 0.

> Gap chỉ được viết vào bài sau khi đọc đủ ≥ 12 bài (gate G2). Còn **740** bản ghi chờ đọc toàn văn trong thư mục này.
