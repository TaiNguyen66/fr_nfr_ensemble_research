"""Lập danh sách đọc ưu tiên (bản 4 tuần) từ kết quả sàng lọc vòng 1 của frnfr-metadata-fetcher.

Chạy (từ gốc repo), sau mỗi lần `cli.mjs screen`:
    python scripts/build_reading_shortlist.py

Đọc literature/search/01_all_records.csv và 02_after_screening_v1.csv,
ghi literature/search/reading-shortlist.csv và reading-shortlist.md.
Đây chỉ là THỨ TỰ ĐỌC gợi ý; quyết định giữ/loại vẫn ghi tay trong review-decisions.csv.
"""

import collections
import csv
import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "literature" / "search"
CORE_STREAMS = {"Q1", "Q1b", "Q2", "Q3", "Q4", "Q5"}

# Paper chuẩn (giống KNOWN_PAPERS của frnfr-metadata-fetcher); so khớp ĐẦU tiêu đề đã chuẩn hoá
KNOWN = [
    "software requirements classification using machine learning algorithms",
    "automatically classifying functional and nonfunctional requirements",
    "what works better",
    "requirements classification with interpretable machine learning",
    "norbert transfer learning",
    "using voting and stacking ensemble",
    "leakage and the reproducibility crisis",
]

# (nhóm, điều kiện, số bài tối đa, lý do)
QUOTAS = [
    ("2 Ensemble (RQ1)", lambda x: inc(x, "CORE-ENSEMBLE"), 10, "INCLUDE · ensemble"),
    ("3 Đánh giá / split / leakage (RQ3)", lambda x: inc(x, "EVALUATION"), 8, "INCLUDE · cách đánh giá"),
    ("1 FR/NFR + ML", lambda x: inc(x, "CORE-ML"), 8, "INCLUDE · CORE-ML, nhiều trích dẫn/năm"),
    ("4 Survey / nền tảng", lambda x: x["decision"] == "BACKGROUND" and core(x) and "Survey" in x["reason"], 4,
     "survey về phân loại yêu cầu"),
    ("4 Survey / nền tảng", lambda x: x["decision"] == "BACKGROUND" and not core(x)
     and re.search(r"leak|duplicat|pitfall|reproducib", x["title"], re.I), 2, "nền tảng leakage (T1)"),
    ("4 Survey / nền tảng", lambda x: x["decision"] == "BACKGROUND" and not core(x)
     and re.search(r"t-test|compar\w* (classifiers|learning algorithms)|cross-validation|significance", x["title"], re.I),
     2, "nền tảng thống kê (T2)"),
    ("5 UNSURE cần quyết", lambda x: x["decision"] == "UNSURE" and x["v2_priority"] == "P1" and core(x), 5,
     "UNSURE nhưng sát RQ (P1)"),
]


def streams(x):
    return {s.strip() for s in x["search_stream"].split(";") if s.strip()}


def core(x):
    return bool(streams(x) & CORE_STREAMS)


def inc(x, tag):
    return x["decision"] == "INCLUDE" and tag in x["reason"]


def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    rows = list(csv.DictReader((DIR / "02_after_screening_v1.csv").open(encoding="utf-8-sig")))
    base = {x["id"]: x for x in csv.DictReader((DIR / "01_all_records.csv").open(encoding="utf-8-sig"))}
    cites = lambda x: int(base[x["id"]].get("cited_by_count") or 0)
    per_year = lambda x: cites(x) / max(1, 2027 - int(x["year"] or 2026))

    picked, seen = [], set()

    def add(x, group, why):
        key = norm(x["title"])[:60]
        if not key or x["id"] in seen or key in seen:
            return False
        seen.update([x["id"], key])
        picked.append((group, why, x))
        return True

    for k in KNOWN:
        hits = sorted((x for x in rows if norm(x["title"]).startswith(k)), key=cites, reverse=True)
        if hits:
            add(hits[0], "0 Paper chuẩn", f"paper nền đã biết (gợi ý tự động: {hits[0]['decision']})")
        else:
            print(f"Cảnh báo: không thấy paper chuẩn '{k}'")
    for group, cond, n, why in QUOTAS:
        added = 0
        for x in sorted((x for x in rows if cond(x)), key=per_year, reverse=True):
            if added >= n:
                break
            added += add(x, group, why)
    picked.sort(key=lambda p: p[0])

    fields = ["rank", "group", "id", "title", "authors", "year", "venue", "doi", "cited_by", "search_stream",
              "auto_decision", "auto_reason", "why_shortlisted"]
    with (DIR / "reading-shortlist.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for i, (g, why, x) in enumerate(picked, 1):
            w.writerow([i, g, x["id"], x["title"], x["authors"][:80], x["year"], x["venue"], x["doi"], cites(x),
                        x["search_stream"], x["decision"], x["reason"], why])

    cell = lambda s, n: s[:n].replace("|", "/")
    md = [
        "# Danh sách đọc ưu tiên (bản 4 tuần)", "",
        "> Sinh bằng `scripts/build_reading_shortlist.py` từ `02_after_screening_v1.csv`. Gợi ý vòng 1 là **tự động**, chưa có người rà.",
        "> Xếp theo nhóm; trong nhóm theo số trích dẫn / năm. Đây là **thứ tự đọc gợi ý**, không phải quyết định giữ/loại.",
        "> Mục tiêu gate G2 (15/10): đọc toàn văn ≥ 12 bài, đủ 4 nhóm. Đọc nhóm 0 trước, rồi 2 và 3 (sát RQ1/RQ3 nhất).", "",
        "| # | Nhóm | ID | Tiêu đề | Năm | Venue | Trích dẫn | Vì sao |",
        "|---:|---|---|---|---:|---|---:|---|",
    ]
    for i, (g, why, x) in enumerate(picked, 1):
        md.append(f"| {i} | {g} | `{x['id']}` | {cell(x['title'], 110)} | {x['year']} | {cell(x['venue'], 40)} | {cites(x)} | {why} |")
    md += ["", "Đọc xong bài nào: ghi dòng `stage=V2` vào `review-decisions.csv`, điền Google Sheet "
           "`literature_matrix_FRNFR`, rồi chạy lại `cli.mjs screen` và script này."]
    (DIR / "reading-shortlist.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"{len(picked)} bài:", dict(collections.Counter(p[0] for p in picked)))
    for i, (g, why, x) in enumerate(picked, 1):
        print(f"{i:>2} [{g[0]}] {x['year']} {cites(x):>4}  {x['title'][:88]}")


if __name__ == "__main__":
    main()
