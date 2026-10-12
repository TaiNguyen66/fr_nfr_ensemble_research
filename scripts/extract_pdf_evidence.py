"""Trích tự động bằng chứng từ PDF bộ bài vòng cuối, phục vụ so sánh và tìm gap (review_protocol.md §7–§8).

Chạy (từ gốc repo, trong .venv có pypdf):
    python scripts/extract_pdf_evidence.py

Đầu vào: literature/review/final_set.csv + literature/pdf/<ID>.pdf
Đầu ra:
    literature/review/pdf_evidence.csv   mỗi bài một dòng: giá trị từng trường + câu trích nguyên văn làm bằng chứng
    literature/review/gap_evidence.md    đếm k/N theo từng trường (đầu vào cho họp tìm gap)

LƯU Ý: đây là dò từ khóa trong phần thân bài (đã cắt phần References), không phải đọc hiểu.
Mỗi giá trị có câu trích để người đọc kiểm tra; số liệu đưa vào bài báo phải được người xác nhận ở tab R3.
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "literature" / "review"

# (trường, {nhãn: regex}) — một bài có thể có nhiều nhãn trong cùng trường
FIELDS = {
    "dataset": {
        # tên dataset phân biệt hoa thường: "promise" / "pure" là từ tiếng Anh thông thường
        "PROMISE_exp": r"(?-i:PROMISE[_ ]?exp|Promise[_ ]?exp|PROMISE[_ ]EXP)|expanded promise",
        "PROMISE (gốc/NFR)": r"(?-i:\bPROMISE\b)(?![_ ]?(exp|EXP))",
        "PURE": r"(?-i:\bPURE\b)",
        "Concordia RE": r"concordia",
        "DOSSPRE / khác công khai": r"dosspre|secreq|dronology|crowdre|leeds",
        "Dữ liệu riêng / tự thu thập": r"(our|own|proprietary|private|collected|industrial) (dataset|data set|corpus)",
    },
    "task": {
        "binary FR/NFR": r"binary classification|(functional|FR) (vs\.?|versus|and) (non[- ]?functional|NFR)|two classes",
        "multi-class NFR": r"multi[- ]?class|11 classes|12 classes|nfr (sub)?(categories|classes|types)",
        "multi-label": r"multi[- ]?label",
    },
    "technique": {
        "ML cổ điển": r"\bsvm\b|support vector|logistic regression|naive bayes|random forest|decision tree|\bknn\b|k-nearest",
        "Ensemble": r"ensemble|\bvoting\b|\bstacking\b|\bbagging\b|boosting|xgboost|adaboost|catboost|lightgbm",
        "Deep learning": r"\bcnn\b|\blstm\b|\bgru\b|\brnn\b|convolutional|recurrent|attention",
        "Transformer / BERT": r"\bbert\b|roberta|transformer|norbert|distilbert",
        "LLM / prompting": r"\bllms?\b|large language model|\bgpt|chatgpt|prompt(ing)?\b|zero[- ]shot|few[- ]shot",
    },
    "representation": {
        "TF-IDF / BoW": r"tf[- ]?idf|bag[- ]of[- ]words|\bbow\b",
        "Word embeddings": r"word2vec|glove|fasttext|word embedding",
        "Contextual embeddings": r"\bbert\b|sentence[- ]?bert|sbert|contextual embedding",
    },
    "preprocessing": {
        "Stopword removal": r"stop[- ]?words?",
        "Lemmatization": r"lemmati",
        "Stemming": r"stemm",
        "Đánh giá riêng ảnh hưởng tiền xử lý": r"(effect|impact|influence) of (the )?(pre-?processing|stop[- ]?word|lemmati|stemm)",
    },
    "split": {
        "k-fold CV": r"\b(\d+|ten|five)[- ]fold|k[- ]fold|cross[- ]validation",
        "Stratified": r"stratif",
        "Train/test split cố định": r"(\d{2})\s?%\s?(for )?(training|train)|train(ing)?[- /]test split|hold[- ]?out",
        "Cross-project / theo project": r"cross[- ]project|leave[- ]one[- ]project|project[- ]wise|p[- ]fold|unseen projects?",
        "Cross-dataset": r"cross[- ]dataset|cross[- ]domain|external (validation|dataset)",
        "Lặp nhiều lần / nhiều seed": r"repeated|(\d+|ten|five) (runs|times|repetitions|seeds)|random seeds?",
    },
    "leakage_control": {
        "Nhắc trùng lặp / leakage": r"duplicat|leakage|near[- ]duplicate|data contamination",
    },
    "metric": {
        "Macro-F1": r"macro[- ]?(averaged )?f1|macro[- ]?f|macro[- ]?average",
        "Weighted-F1": r"weighted[- ]?(averaged )?f1|weighted[- ]?average",
        "Micro-F1": r"micro[- ]?(averaged )?f1|micro[- ]?average",
        "F1 theo lớp": r"(per|each)[- ]class|class[- ]wise|class[- ]level",
        "Accuracy": r"\baccuracy\b",
    },
    "stat_test": {
        "Có kiểm định thống kê": r"t[- ]test|wilcoxon|friedman|mcnemar|scott[- ]knott|nemenyi|mann[- ]whitney|statistically significant|p[- ]?value|confidence interval",
    },
    "reproducibility": {
        "Có link code/data": r"github\.com|gitlab|zenodo|figshare|replication package|code (is|are) (publicly )?available|available at https?://",
    },
    "imbalance": {
        "Xử lý mất cân bằng": r"smote|oversampl|undersampl|class imbalance|imbalanced|class weight",
    },
}


def body_text(pdf_path, max_pages=30):
    try:
        reader = PdfReader(str(pdf_path))
        text = "\n".join((p.extract_text() or "") for p in reader.pages[:max_pages])
    except Exception as err:
        return "", f"lỗi đọc PDF: {err}"
    text = re.sub(r"-\n(?=[a-z])", "", text)        # nối chữ bị ngắt dòng
    text = re.sub(r"\s+", " ", text)
    cut = [m.start() for m in re.finditer(r"\b(References|REFERENCES|Bibliography)\b", text)]
    if cut and cut[-1] > len(text) * 0.5:          # chỉ cắt khi mục References nằm ở nửa sau
        text = text[:cut[-1]]
    return text, ""


def evidence(text, pattern):
    m = re.search(pattern, text, re.I)
    if not m:
        return ""
    start = max(0, text.rfind(". ", 0, m.start()) + 2)
    end = text.find(". ", m.end())
    end = len(text) if end == -1 else end + 1
    return text[start:end][:300].strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    papers = list(csv.DictReader((REVIEW / "final_set.csv").open(encoding="utf-8-sig")))
    rows = []
    for p in papers:
        text, err = body_text(ROOT / p["pdf"])
        row = {"id": p["id"], "group": p["group"], "title": p["title"], "year": p["year"], "chars": len(text), "error": err}
        for field, labels in FIELDS.items():
            hits = [lab for lab, rx in labels.items() if text and re.search(rx, text, re.I)]
            row[field] = "; ".join(hits)
            first = next((evidence(text, labels[lab]) for lab in hits), "")
            row[f"{field}_evidence"] = first
        rows.append(row)
        print(f"{p['id']} {len(text):>7} ký tự  {p['title'][:60]}")

    with (REVIEW / "pdf_evidence.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    ok = [r for r in rows if r["chars"] > 3000]
    n = len(ok)
    md = ["# Bằng chứng tự động từ PDF (đầu vào cho họp tìm gap)", "",
          f"> Sinh bằng `scripts/extract_pdf_evidence.py` từ {n} PDF đọc được (trên {len(rows)} bài vòng cuối).",
          "> Dò từ khóa trong phần thân bài, **chưa được người kiểm tra**. Dùng để định hướng; số đưa vào bài phải xác nhận ở tab R3.", ""]
    for field, labels in FIELDS.items():
        md += [f"## {field}", "", "| Nhãn | Số bài | Tỉ lệ |", "|---|---:|---:|"]
        c = Counter(lab for r in ok for lab in r[field].split("; ") if lab)
        for lab in labels:
            md.append(f"| {lab} | {c[lab]} | {c[lab] / n:.0%} |" if n else f"| {lab} | 0 | – |")
        md.append("")
    # Các tổ hợp gợi ý gap
    kfold_no_leak = [r for r in ok if "k-fold" in r["split"] and not r["leakage_control"] and "Cross-project" not in r["split"]]
    ens_no_stat = [r for r in ok if "Ensemble" in r["technique"] and not r["stat_test"]]
    no_code = [r for r in ok if not r["reproducibility"]]
    md += ["## Tổ hợp gợi ý gap (kiểm tra lại bằng tay)", "",
           f"- Dùng k-fold nhưng không nhắc trùng lặp/leakage và không chia theo project: **{len(kfold_no_leak)}/{n}**",
           f"- Dùng ensemble nhưng không có kiểm định thống kê: **{len(ens_no_stat)}/{sum(1 for r in ok if 'Ensemble' in r['technique'])}** bài ensemble",
           f"- Không có link code/data: **{len(no_code)}/{n}**", ""]
    (REVIEW / "gap_evidence.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"\nĐọc được {n}/{len(rows)} PDF. Ghi pdf_evidence.csv và gap_evidence.md")


if __name__ == "__main__":
    main()
