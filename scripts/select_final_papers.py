"""Lọc nhanh tới bộ bài vòng cuối (amendment A-004): chỉ giữ bài liên quan, bình duyệt, có abstract và TẢI ĐƯỢC PDF.

Chạy (từ gốc repo):
    python scripts/select_final_papers.py                  # lọc + tra OpenAlex + tải PDF, dừng ở 30 bài
    python scripts/select_final_papers.py --target 25
    python scripts/select_final_papers.py --no-download    # chỉ lọc, không tải

Đầu vào: literature/search/01_all_records.csv, 02_after_screening_v1.csv
Đầu ra:
    literature/review/final_candidates.csv   mọi bài qua lọc nội dung + trạng thái PDF + lý do loại
    literature/review/final_set.csv          bài vòng cuối (có PDF) để đọc và tìm gap
    literature/pdf/<ID>.pdf                  PDF đã tải (gitignored, không commit)

Luật lọc (theo yêu cầu đẩy nhanh, 2026-10-12):
    L1 gợi ý tự động là INCLUDE (core) hoặc thuộc danh sách nền tảng cần cho đề tài; loại UNSURE / EXCLUDE
    L2 có abstract (≥ 200 ký tự)
    L3 bình duyệt: journal / conference; loại preprint, luận văn, sách, khác
    L4 liên quan: nhắc FR/NFR (hoặc PROMISE) và phân loại yêu cầu trong cùng câu; loại văn bản khác (app review, issue, legal)
    L5 tải được PDF hợp lệ (bắt đầu bằng %PDF) NGAY lần thử đầu: một link duy nhất, chờ tối đa 10 giây.
       Bị chặn / đòi xác nhận bot / trả về trang HTML → bỏ qua, không thử link khác.
Chọn bài: luân phiên các nhóm CORE-ENSEMBLE → EVALUATION → CORE-ML (BACKGROUND tối đa 4),
trong nhóm theo trích dẫn/năm; dừng khi đủ --target bài có PDF (mặc định 30).
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "literature" / "search"
OUT = ROOT / "literature" / "review"
PDF_DIR = ROOT / "literature" / "pdf"
CORE = {"Q1", "Q1b", "Q2", "Q3", "Q4", "Q5"}

# Bài nền tảng giữ lại dù gợi ý tự động là BACKGROUND (survey phân loại yêu cầu + khung lý thuyết leakage)
BACKGROUND_KEEP = re.compile(
    r"leakage and the reproducibility crisis|adverse effects of code duplication|"
    r"review of machine learning algorithms for identification and classification of non-functional|"
    r"application of ai techniques in requirements classification|"
    r"machine learning techniques for requirements engineering: a comprehensive", re.I)

FRNFR = re.compile(r"non[- ]?functional|functional requirements?|\bNFRs?\b|quality (requirements?|attributes?)|PROMISE", re.I)
REQ_CLASSIF = re.compile(r"(requirement|NFR|non[- ]?functional).{0,80}(classif|categori)|(classif|categori).{0,80}(requirement|NFR)", re.I)
OTHER_TEXT = re.compile(r"app (store )?reviews?|app stores?|user (feedback|reviews?)|tweets?|issue (reports?|trackers?)|bug reports?|"
                        r"stack overflow|privacy polic|legal|regulat|contract", re.I)
UA = {"User-Agent": "frnfr-research/1.0 (academic literature review; open-access PDFs only)"}


def streams(x):
    return {s.strip() for s in x["search_stream"].split(";") if s.strip()}


def content_filter(x, rec):
    """Trả về (giữ?, lý do loại)."""
    text = f"{x['title']} {x['abstract']}"
    background = bool(BACKGROUND_KEEP.search(x["title"]))
    if not background:
        if x["decision"] != "INCLUDE" or not streams(x) & CORE:
            return False, f"L1 gợi ý tự động {x['decision']}"
    if len(x["abstract"]) < 200:
        return False, "L2 thiếu abstract"
    if rec.get("doc_type") not in ("journal", "conference"):
        return False, f"L3 không bình duyệt ({rec.get('doc_type')})"
    if background:
        return True, ""
    if not FRNFR.search(text) or not REQ_CLASSIF.search(text):
        return False, "L4 không rõ là phân loại FR/NFR"
    if OTHER_TEXT.search(x["title"]):
        return False, "L4 văn bản khác (review / issue / pháp lý)"
    return True, ""


def first_pdf_url(doi, title, fallback):
    """MỘT link PDF: pdf_url của best_oa_location trên OpenAlex; không có thì dùng oa_url đã lưu."""
    if doi:
        url = "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)
    else:
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"filter": f"title.search:{title[:200]}", "per_page": 1})
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15) as r:
            data = json.load(r)
        work = data["results"][0] if "results" in data and data["results"] else data
        pdf = (work.get("best_oa_location") or {}).get("pdf_url")
        if pdf:
            return pdf
    except Exception:
        pass
    return fallback or ""


def try_once(url, dest):
    """Một lần thử, 10 giây. Trả về lý do thất bại, hoặc "" nếu tải được PDF hợp lệ."""
    if not url:
        return "không có link open access"
    try:
        req = urllib.request.Request(url, headers={**UA, "Accept": "application/pdf"})
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read(25_000_000)
    except Exception as err:
        return f"không tải được ({type(err).__name__})"
    if body[:5] != b"%PDF-":
        return "không phải PDF (trang web / xác nhận bot)"
    dest.write_bytes(body)
    return ""


def main():
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)  # console Windows mặc định cp1252
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=30, help="số bài có PDF cần đạt")
    ap.add_argument("--max-background", type=int, default=4)
    ap.add_argument("--exclude", default="", help="ID bị người duyệt loại vì lạc đề, cách nhau bằng dấu phẩy")
    args = ap.parse_args()
    excluded = {e.strip() for e in args.exclude.split(",") if e.strip()}

    base = {x["id"]: x for x in csv.DictReader((SRC / "01_all_records.csv").open(encoding="utf-8-sig"))}
    rows = list(csv.DictReader((SRC / "02_after_screening_v1.csv").open(encoding="utf-8-sig")))
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    per_year = lambda x: int(base[x["id"]].get("cited_by_count") or 0) / max(1, 2027 - int(x["year"] or 2026))
    groups = {"CORE-ENSEMBLE": [], "EVALUATION": [], "CORE-ML": [], "BACKGROUND": []}
    for x in rows:
        ok, _ = content_filter(x, base[x["id"]])
        if not ok:
            continue
        g = ("BACKGROUND" if BACKGROUND_KEEP.search(x["title"]) else
             "CORE-ENSEMBLE" if "CORE-ENSEMBLE" in x["reason"] else
             "EVALUATION" if "EVALUATION" in x["reason"] else "CORE-ML")
        groups[g].append(x)
    for g in groups:
        groups[g].sort(key=per_year, reverse=True)
    print("Qua lọc nội dung L1–L4:", {g: len(v) for g, v in groups.items()})

    # Bài nền tảng trước (ít, cần cho khung lý thuyết), rồi luân phiên ba nhóm chính
    order = [("BACKGROUND", x) for x in groups["BACKGROUND"]]
    queues = [list(groups[g]) for g in ("CORE-ENSEMBLE", "EVALUATION", "CORE-ML")]
    names = ["CORE-ENSEMBLE", "EVALUATION", "CORE-ML"]
    while any(queues):
        for name, q in zip(names, queues):
            if q:
                order.append((name, q.pop(0)))

    out, final, bg = [], 0, 0
    for g, x in order:
        rec = base[x["id"]]
        pdf = PDF_DIR / f"{x['id']}.pdf"
        status = ""
        if x["id"] in excluded:
            status = "DROP L4 lạc đề (người duyệt loại)"
        elif final >= args.target or (g == "BACKGROUND" and bg >= args.max_background):
            status = "NOT_TRIED (đã đủ số lượng)"
        elif pdf.exists():
            status = "FINAL"
        else:
            why = try_once(first_pdf_url(x["doi"], x["title"], rec.get("oa_url")), pdf)
            status = "FINAL" if not why else f"DROP L5 {why}"
            print(f"{x['id']} [{g}] {'PDF' if not why else '---'} {x['title'][:65]}")
        if status == "FINAL":
            final += 1
            bg += g == "BACKGROUND"
        out.append({"id": x["id"], "group": g, "title": x["title"], "authors": x["authors"], "year": x["year"],
                    "venue": x["venue"], "doi": x["doi"], "cited_by": rec.get("cited_by_count", ""),
                    "pdf": f"literature/pdf/{x['id']}.pdf" if status == "FINAL" else "", "status": status,
                    "abstract": x["abstract"]})

    fields = list(out[0].keys())
    with (OUT / "final_candidates.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    fin = [r for r in out if r["status"] == "FINAL"]
    with (OUT / "final_set.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(fin)
    from collections import Counter
    print(f"\nVòng cuối: {len(fin)} bài có PDF", dict(Counter(r["group"] for r in fin)))
    print("Bị loại L5:", sum(1 for r in out if r["status"].startswith("DROP")),
          "· chưa thử vì đã đủ:", sum(1 for r in out if r["status"].startswith("NOT_TRIED")))


if __name__ == "__main__":
    main()
