# Bằng chứng tự động từ PDF (đầu vào cho họp tìm gap)

> Sinh bằng `scripts/extract_pdf_evidence.py` từ 30 PDF đọc được (trên 30 bài vòng cuối).
> Dò từ khóa trong phần thân bài, **chưa được người kiểm tra**. Dùng để định hướng; số đưa vào bài phải xác nhận ở tab R3.

## dataset

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| PROMISE_exp | 7 | 23% |
| PROMISE (gốc/NFR) | 23 | 77% |
| PURE | 11 | 37% |
| Concordia RE | 0 | 0% |
| DOSSPRE / khác công khai | 5 | 17% |
| Dữ liệu riêng / tự thu thập | 11 | 37% |

## task

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| binary FR/NFR | 26 | 87% |
| multi-class NFR | 21 | 70% |
| multi-label | 7 | 23% |

## technique

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| ML cổ điển | 27 | 90% |
| Ensemble | 19 | 63% |
| Deep learning | 25 | 83% |
| Transformer / BERT | 16 | 53% |
| LLM / prompting | 8 | 27% |

## representation

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| TF-IDF / BoW | 21 | 70% |
| Word embeddings | 19 | 63% |
| Contextual embeddings | 15 | 50% |

## preprocessing

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| Stopword removal | 19 | 63% |
| Lemmatization | 11 | 37% |
| Stemming | 11 | 37% |
| Đánh giá riêng ảnh hưởng tiền xử lý | 0 | 0% |

## split

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| k-fold CV | 11 | 37% |
| Stratified | 7 | 23% |
| Train/test split cố định | 8 | 27% |
| Cross-project / theo project | 7 | 23% |
| Cross-dataset | 5 | 17% |
| Lặp nhiều lần / nhiều seed | 14 | 47% |

## leakage_control

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| Nhắc trùng lặp / leakage | 9 | 30% |

## metric

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| Macro-F1 | 2 | 7% |
| Weighted-F1 | 6 | 20% |
| Micro-F1 | 2 | 7% |
| F1 theo lớp | 17 | 57% |
| Accuracy | 28 | 93% |

## stat_test

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| Có kiểm định thống kê | 12 | 40% |

## reproducibility

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| Có link code/data | 10 | 33% |

## imbalance

| Nhãn | Số bài | Tỉ lệ |
|---|---:|---:|
| Xử lý mất cân bằng | 18 | 60% |

## Tổ hợp gợi ý gap (kiểm tra lại bằng tay)

- Dùng k-fold nhưng không nhắc trùng lặp/leakage và không chia theo project: **8/30**
- Dùng ensemble nhưng không có kiểm định thống kê: **14/19** bài ensemble
- Không có link code/data: **20/30**

