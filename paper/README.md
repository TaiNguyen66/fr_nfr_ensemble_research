# Paper kit

| File | Dùng để |
|---|---|
| `main.tex` | File chính (IEEEtran, 2 cột, pdfLaTeX + BibTeX) |
| `sections/*.tex` | Mỗi section một file; thay các dòng `TODO` |
| `tables/*.tex`, `figures/summary_deltas.pdf` | **Sinh tự động** bằng `python -m src.paper_tables`; không sửa tay |
| `figures/design.tex` | Sơ đồ thiết kế (TikZ) |
| `figures/slide_rq2_t12.png`, `summary_deltas.png` | Hình cho slide |
| `references.bib` | 43 mục; 40 mục lấy từ DOI (Crossref), 3 mục gõ tay (`holm1979`, `pedregosa2011`, `lemaitre2017`) |
| `fact_sheet.md` | Nguồn sự thật duy nhất cho mọi con số và cách diễn đạt |
| `AGENT_PROMPTS.md` | Prompt cho ChatGPT / Gemini theo từng section |
| `SLIDES_PLAN.md` | Dàn ý 17 slide cho Canva |
| `results_skeleton.md` | Khung Results cũ và nhật ký kiểm chứng chạy lại |

## Đưa lên Overleaf

1. Nén **nội dung** thư mục `paper/` thành `paper.zip`, sao cho `main.tex` nằm ở gốc file zip. Không cần đưa các file `.md` lên.
2. Overleaf → *New Project* → *Upload Project* → chọn `paper.zip`.
3. *Menu* → Compiler: **pdfLaTeX**; Main document: `main.tex`. Bấm *Recompile*. Bản đầu sẽ có chữ TODO, đó là bình thường.
4. *Share* → thêm e-mail của Hoang Anh với quyền *Can edit*.
5. Nếu bảng hoặc hình thay đổi: chạy lại `python -m src.paper_tables` trên máy rồi upload đè các file trong `tables/` và `figures/` trên Overleaf.

## Ghi chú

- Kiểm tra lại thông tin của 3 mục bib gõ tay và mục `ali2025multi` (DOI không tra được trên Crossref, thông tin lấy từ bảng review).
- Phần Error analysis chỉ viết sau khi đã gán nhãn 30 dòng trong `results/predictions/error_analysis_sample.csv`.
