# Hướng dẫn chạy thí nghiệm, theo dõi và ghi nhận kết quả

Dành cho: Hoang Anh, Phat Tai. Lệnh viết cho **PowerShell trên Windows**, chạy trong thư mục repo `fr_nfr_ensemble_research`.

> **Quy tắc quan trọng nhất:** không chạy model nào trước khi protocol LOCKED. Script tự kiểm tra và sẽ dừng nếu `protocol/research_protocol.md` chưa ghi `| Status | **LOCKED**`.

## 0. Tóm tắt nhanh

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q tests                          # 1. test phải qua hết
python -m src.audit_dataset                        # 2. sinh dữ liệu đã xử lý
python -m src.run_experiments --plan RQ1 *>&1 | Tee-Object logs\run_RQ1.txt   # 3. chạy
python -m src.run_experiments --plan RQ2 *>&1 | Tee-Object logs\run_RQ2.txt
python -m src.run_experiments --plan D2  *>&1 | Tee-Object logs\run_D2.txt
```

Sau đó ghi nhận kết quả theo mục 5 và commit theo mục 6.

---

## 1. Chuẩn bị máy (làm một lần)

### 1.1 Môi trường Python

Cần Python 3.12.

```powershell
git clone https://github.com/TaiNguyen66/fr_nfr_ensemble_research.git
cd fr_nfr_ensemble_research
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Nếu PowerShell báo không cho chạy `Activate.ps1`: chạy `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` một lần, rồi thử lại.

### 1.2 Dữ liệu thô (không có trên GitHub)

File thô không đưa lên GitHub. Lấy từ máy Phat Tai, hoặc tải lại:

| File cần có | Nguồn |
|---|---|
| `data/raw/PROMISE_exp.arff` | https://github.com/AleksandarMitrevski/se-requirements-classification/tree/master/0-datasets/PROMISE_exp |
| `data/raw/dalpiaz2019/dronology.csv`, `leeds.csv`, `reqview.csv`, `wasp.csv` | https://zenodo.org/records/3309582 → tải `RE2019-Paper96.zip` → giải nén → thư mục `Manually tagged datasets/` |

**Không mở các file này bằng Excel rồi lưu lại**, vì Excel làm đổi nội dung và mã SHA-256.

### 1.3 Kiểm tra dữ liệu đúng bản đã freeze

```powershell
Get-FileHash data\raw\PROMISE_exp.arff -Algorithm SHA256
Get-ChildItem data\raw\dalpiaz2019\*.csv | Get-FileHash -Algorithm SHA256
```

So với cột `sha256` trong `data/checksums.csv`. Có file nào khác thì **dừng lại**, báo cho người kia; không chạy tiếp.

---

## 2. Kiểm tra trước khi chạy

### 2.1 Chạy test

```powershell
python -m pytest -q tests
```

Kết quả phải là `28 passed` (hoặc nhiều hơn nếu đã thêm test). Có test fail thì không chạy thí nghiệm.

### 2.2 Sinh dữ liệu đã xử lý

```powershell
python -m src.audit_dataset
```

Kết quả đúng phải in ra:

```
PROMISE_exp: 969 rows, 47 projects, {'NFR': 525, 'FR': 444}, 12 classes
  near-duplicate candidates >= 0.9: 14; SAME merged: 5
  duplicate groups with > 1 row: 8 (16 rows); label conflicts (bin): 0
  groups crossing folds under S (5 seeds): [6, 7, 8, 7, 6]
Dalpiaz2019: 327 rows, {'FR': 187, 'NFR': 140}, duplicate rows: 0
Dalpiaz2019 (no both): 246 rows, {'FR': 187, 'NFR': 59}, duplicate rows: 0
```

Lệnh này tạo 3 file trong `data/processed/` (`requirements.csv`, `dalpiaz_requirements.csv`, `dalpiaz_requirements_noboth.csv`). Các file này chứa text nên đã nằm trong `.gitignore`.

### 2.3 Protocol đã LOCKED chưa

Mở `protocol/research_protocol.md`, dòng Status phải là `| Status | **LOCKED** ...`. Đồng thời mục §14 có chữ ký của cả hai người, và `protocol/amendment_log.md` có ☑ của cả hai ở A-003 đến A-007.

### 2.4 Code đã commit hết chưa

```powershell
git status
```

Phải sạch (không có file `.py` chưa commit). Log thí nghiệm ghi lại mã commit; nếu code chưa commit thì không ai tái lập được kết quả.

---

## 3. Chạy thí nghiệm

### 3.1 Ba kế hoạch chạy

| Lệnh `--plan` | Phục vụ | Dữ liệu | Số cấu hình | Seed |
|---|---|---|---|---|
| `RQ1` | RQ1 (câu trùng, project) **và RQ3** (ensemble) | PROMISE_exp, T-bin | 7 model × 3 cách chia (S, G-dup, G-proj) = 21 | 5 seed × 5 fold |
| `RQ2` | RQ2 (oversampling trước và trong fold) | PROMISE_exp, T-bin và T-12 | 2 task × 5 model × 5 điều kiện = 50 | 5 seed × 5 fold |
| `D2` | Kiểm tra lại trên Dalpiaz2019 (A-007) | 4 bộ Dalpiaz, T-bin | 5 model × 7 = 35 | 5 seed × 5 fold; LODO chạy 1 lần × 4 fold |

Chạy theo thứ tự **RQ1 → RQ2 → D2**. RQ1 nhanh nhất, dùng để kiểm tra mọi thứ hoạt động trước khi chạy phần nặng.

### 3.2 Lệnh chạy và lưu log ra file

```powershell
New-Item -ItemType Directory -Force logs | Out-Null
python -m src.run_experiments --plan RQ1 --owner phat-tai *>&1 | Tee-Object logs\run_RQ1.txt
```

- `--owner`: `phat-tai` hoặc `hoang-anh`, là người chạy; được ghi vào `experiments/experiment_log.csv`.
- `Tee-Object` vừa in ra màn hình vừa lưu vào `logs\run_RQ1.txt`, nên tắt cửa sổ vẫn còn log.
- Thư mục `logs/` chỉ để theo dõi, không commit.

### 3.3 Thời gian chạy

Chưa đo trên dữ liệu thật. Ước lượng thô: RQ1 khoảng vài chục phút, RQ2 lâu nhất (Random Forest và Voting trên 12 lớp, cộng SMOTE), D2 nhanh vì dữ liệu nhỏ. **Ghi lại thời gian thực tế** vào `research_log.md` để lần chạy lại ngày 02/11 biết trước.

Trong lúc chạy: cắm sạc, tắt chế độ ngủ của máy (Settings → System → Power → Sleep: Never), không chạy việc nặng khác.

---

## 4. Theo dõi khi đang chạy

### 4.1 Đọc dòng tiến độ

Mỗi cấu hình chạy xong (đủ 5 seed) in một dòng:

```
[3/21] requirements.csv T-bin M0 G-proj NONE : macro-F1 0.351 (last seed)
```

| Phần | Nghĩa |
|---|---|
| `[3/21]` | cấu hình thứ 3 trên 21 |
| `requirements.csv` | dữ liệu (PROMISE_exp); `dalpiaz_requirements*.csv` là Dalpiaz |
| `T-bin` / `T-12` | bài toán FR/NFR hay 12 lớp |
| `M0`…`M6` | model |
| `S` / `G-dup` / `G-proj` / `LODO` | cách chia |
| `NONE` / `IN-FOLD` / `BEFORE` + `OS-R` / `OS-S` | điều kiện oversampling |
| `macro-F1 ... (last seed)` | trung bình 5 fold của **seed cuối**, chỉ để theo dõi; không dùng làm kết quả |

Xem log từ cửa sổ khác:

```powershell
Get-Content logs\run_RQ2.txt -Wait -Tail 5
```

### 4.2 Dấu hiệu bình thường và bất thường

| Quan sát | Bình thường? | Làm gì |
|---|---|---|
| M0 (Dummy) T-bin có macro-F1 ≈ 0,35 | Bình thường (luôn đoán NFR) | – |
| M1–M6 T-bin dưới cách chia S khoảng 0,7–0,9 | Bình thường | – |
| G-proj thấp hơn S | Đúng giả thuyết | Ghi lại, không kết luận khi chưa có kiểm định |
| BEFORE cao hơn IN-FOLD | Đúng giả thuyết | Như trên |
| Kết quả ngược giả thuyết (G-proj ≥ S, BEFORE ≤ IN-FOLD) | **Vẫn là kết quả hợp lệ** | Ghi lại; **không** sửa code hay chạy lại để "đẹp" hơn |
| Model nào đó có macro-F1 > 0,99 hoặc < 0,3 (trừ M0) | Đáng ngờ | Dừng, báo người kia, kiểm tra trước khi chạy tiếp |
| Lỗi `AssertionError: ... in both train and test` | Lỗi rò rỉ, code chặn lại | Dừng, báo lỗi (xem mục 7) |
| Cảnh báo `ConvergenceWarning` của LinearSVC | Thường gặp, không phải lỗi | Ghi vào log ngày; không đổi tham số |

### 4.3 Bị ngắt giữa chừng

Script **không** chạy tiếp từ chỗ dừng. Kết quả chỉ được ghi ra file khi cả kế hoạch chạy xong, nên nếu bị ngắt (mất điện, tắt máy) thì chạy lại cả lệnh `--plan` đó. Kết quả giống hệt vì seed cố định. Ghi việc bị ngắt vào `research_log.md`.

---

## 5. Kết quả nằm ở đâu và ghi nhận thế nào

### 5.1 File kết quả của mỗi lần chạy

| File | Nội dung | Commit? |
|---|---|---|
| `results/tables/fold_scores_<PLAN>.csv` | Một dòng cho mỗi fold: `dataset, task, model, protocol, condition, oversampler, seed, fold, n_train, n_test, macro_f1, accuracy, macro_precision, macro_recall` | **Có**, đây là số liệu gốc cho kiểm định |
| `results/predictions/predictions_<PLAN>.csv` | Một dòng cho mỗi câu test: `row_id, project_id, duplicate_group, true_label, predicted_label, score, fold, seed, task, model, protocol, oversampling` | **Có** (không chứa text) |
| `results/splits/splits_<PLAN>.csv` | Câu nào ở fold nào, theo từng cách chia và seed | **Có** |
| `experiments/experiment_log.csv` | Mỗi lần chạy thêm 1 dòng: mã chạy, thời điểm, người chạy, commit, SHA-256 dữ liệu, plan, seed, phiên bản thư viện | **Có** |
| `logs/run_<PLAN>.txt` | Log màn hình | Không |

Chạy lại cùng plan sẽ **ghi đè** các file trong `results/`. File `experiment_log.csv` chỉ thêm dòng, không ghi đè.

### 5.2 Xem nhanh kết quả trung bình

Trong khi chờ script tổng hợp chính thức, dùng lệnh này để xem macro-F1 trung bình của mỗi cấu hình (25 fold):

```powershell
python -c "import pandas as pd; d=pd.read_csv('results/tables/fold_scores_RQ1.csv'); print(d.groupby(['task','model','protocol','condition','oversampler'],dropna=False).macro_f1.agg(['mean','std','count']).round(3).to_string())"
```

Cột `count` phải là 25 (LODO là 4). Khác số này nghĩa là có cấu hình bị thiếu fold.

Số trong bảng này chỉ là **mô tả**. Kết luận "A tốt hơn B" chỉ được dùng sau khi chạy kiểm định (corrected t-test + Holm, quy tắc ở protocol §10).

### 5.3 Ghi vào `research_log.md`

Mỗi lần chạy thêm một mục theo mẫu sẵn trong file:

```text
## 2026-10-18 — Phat Tai
Done (link file/commit): chạy --plan RQ1 (experiment_id a1b2c3d4, commit abc1234), 21 cấu hình, 52 phút.
  results/tables/fold_scores_RQ1.csv
Blockers: không
Decisions (amendment ID nếu đổi scope): không
Next: chạy --plan RQ2
Needs review from: Hoang Anh (kiểm tra bảng trung bình mục 5.2)
```

Ghi các điểm sau:
- `experiment_id`: lấy ở dòng cuối của `experiments/experiment_log.csv`.
- Mã commit: lấy bằng `git rev-parse --short HEAD`.
- Thời gian chạy thực tế.
- Những gì bất thường (mục 4.2), kể cả khi đã tự xử lý.

### 5.4 Người kia kiểm tra lại

Người không chạy mở `fold_scores_<PLAN>.csv`, chạy lệnh ở mục 5.2 và kiểm tra:
- [ ] Đủ số cấu hình (21 / 50 / 35) và mỗi cấu hình đủ 25 fold (LODO: 4).
- [ ] M0 có macro-F1 khoảng 0,35 (T-bin).
- [ ] Không có giá trị trống hoặc bằng 0 bất thường.
- [ ] `experiment_log.csv` có dòng mới, đúng người chạy và commit.

---

## 6. Commit kết quả

```powershell
git add results/tables results/predictions results/splits experiments/experiment_log.csv research_log.md
git status            # kiểm tra không có file data/raw hoặc data/processed/*.csv có text
git commit -m "Run RQ1 (experiment a1b2c3d4)"
git push
```

Không commit `data/raw/`, `data/processed/requirements.csv`, `data/processed/dalpiaz_requirements*.csv`, `logs/`.

---

## 7. Khi có lỗi hoặc muốn thay đổi

| Tình huống | Làm gì |
|---|---|
| Script dừng với lỗi Python | Lưu `logs\run_<PLAN>.txt`, ghi vào `research_log.md` (Blockers), báo người kia. Không sửa code cho chạy qua khi chưa hiểu lỗi |
| Phải sửa code (lỗi thật) | Sửa, thêm test cho lỗi đó, chạy `pytest`, commit, rồi **chạy lại cả plan** bị ảnh hưởng. Ghi mã commit cũ và mới vào log |
| Muốn đổi model, tham số, metric, cách chia, dữ liệu | **Không được** đổi tùy ý. Phải thêm amendment mới vào `protocol/amendment_log.md`, cả hai người đồng ý trước, rồi mới chạy |
| Kết quả không như mong đợi | Báo cáo đúng như vậy. Không chạy thêm seed, không bỏ model, không đổi ngưỡng để kết quả "đẹp" hơn |
| Chạy lại để kiểm tra tái lập (02/11) | Dùng đúng commit đã ghi; số trong `fold_scores` phải giống hệt lần trước. Khác thì ghi lại và tìm nguyên nhân |

---

## 8. Checklist cho mỗi lần chạy

- [ ] SHA-256 dữ liệu thô khớp `data/checksums.csv`
- [ ] `pytest` qua hết
- [ ] `audit_dataset` in đúng số liệu ở mục 2.2
- [ ] Protocol LOCKED
- [ ] `git status` sạch, code đã push
- [ ] Chạy plan với `--owner` đúng tên, log ra `logs\`
- [ ] Kiểm tra bảng trung bình (mục 5.2): đủ cấu hình, đủ fold
- [ ] Ghi `research_log.md` (experiment_id, commit, thời gian, bất thường)
- [ ] Commit `results/`, `experiment_log.csv`, `research_log.md`
- [ ] Người kia kiểm tra lại (mục 5.4)

## 9. Phân tích kết quả

Sau khi chạy xong các plan (không cần đủ cả 3, script bỏ qua plan chưa có file):

```powershell
.venv\Scripts\python -m src.analyze_results            # thêm --no-figures nếu chỉ cần bảng
```

Kết quả trong `results/tables/`:

- `stats_<họ>.csv` chỉ cho **RQ3-Gdup** và **RQ3-S** (các model dùng chung split): mean Δ (A − B theo cột `comparison`), SD, t, p, CI 95% chưa hiệu chỉnh, `p_holm`, `decision` (quy tắc §10: |Δ| ≥ 0.01 và Holm p < 0.05). Ghép cặp theo (seed, fold); tỷ lệ `n_test/n_train` lấy từ các fold thật.
- `descriptive_<họ>.csv` cho **RQ1-dup, RQ1-proj, RQ2-bin, RQ2-12, RQ2-D2** (A-009): mean và SD của từng bên, Δ = hiệu hai trung bình. **Không** có p-value vì hai bên không cùng tập test.
- `summary_<plan>.csv`: mean/SD macro-F1 từng cấu hình.
- `descriptive_none_vs_infold_<plan>.csv`: NONE vs IN-FOLD (chỉ mô tả).
- `descriptive_RQ1-D2_S_vs_LODO.csv`: S (25 fold) vs LODO (4 fold) trên Dalpiaz, chỉ mô tả.
- `kendall_tau.csv`: τ giữa xếp hạng model S vs G-dup, S vs G-proj (PROMISE_exp) và S vs LODO (Dalpiaz).

Hình trong `results/figures/delta_RQ3-*.png`: Δ và CI 95%; chấm đặc = khác biệt rõ, chấm rỗng = không khác biệt rõ.

Sinh bảng và hình cho bài báo (`paper/tables/*.tex`, `paper/figures/summary_deltas.*`):

```powershell
.venv\Scripts\python -m src.paper_tables
```

Lưu ý: điều kiện BEFORE chia fold trên tập đã oversample, nên fold của BEFORE và IN-FOLD không cùng dòng test; vì vậy RQ2 chỉ báo cáo mô tả (A-009).
