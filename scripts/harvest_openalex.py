"""Thu metadata paper từ OpenAlex cho phần literature (Phase 2).

Chạy (từ gốc repo):
    python scripts/harvest_openalex.py                 # Q1, Q1b, Q2–Q5, 100 bản ghi/query
    python scripts/harvest_openalex.py --queries Q1,Q2 --max 200

Đầu ra trong literature/:
    01_openalex_screening.csv      một dòng / paper (đã dedup), cột sàng lọc để nhóm điền tay
    openalex_search_manifest.json  từng lần chạy: query, filter, ngày, tổng số kết quả, số đã lấy
    search-log.md                  nhật ký chỉ thêm, dùng cho mục Method của paper

Chạy lại sẽ GỘP vào CSV cũ: giữ nguyên các cột đã sàng lọc tay, chỉ thêm paper mới
và cập nhật matched_queries. API key (tùy chọn) lấy từ biến môi trường OPENALEX_API_KEY,
không bao giờ ghi vào file.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TOOL_VERSION = "1.0"
API = "https://api.openalex.org/works"
OUT_DIR = Path(__file__).resolve().parent.parent / "literature"
CSV_PATH = OUT_DIR / "01_openalex_screening.csv"
MANIFEST_PATH = OUT_DIR / "openalex_search_manifest.json"
LOG_PATH = OUT_DIR / "search-log.md"

# Chuỗi tìm trên title + abstract. Muốn đổi chuỗi: thêm query mới (Q1b, ...) thay vì sửa chuỗi cũ,
# để search-log còn đối chiếu được.
QUERIES = {
    "Q1": ("Core FR/NFR",
           '("functional requirements" OR "non-functional requirements" OR "nonfunctional requirements" '
           'OR "quality requirements") AND (classification OR classifying OR classifier)'),
    # Bổ sung Q1 (thêm 2026-10-09): bài viết "functional and non-functional (quality) requirements"
    # không khớp cụm từ của Q1, vd Dalpiaz et al. 2019
    "Q1b": ("Requirements classification + ML",
            '("requirements classification" OR "requirement classification" OR "classifying requirements" '
            'OR "classification of requirements") AND ("machine learning" OR "deep learning" OR classifier '
            'OR classifiers OR "natural language processing" OR NLP)'),
    "Q2": ("Ensemble",
           '("requirements classification" OR "requirement classification" OR "classifying requirements") '
           'AND (ensemble OR voting OR stacking OR bagging OR boosting)'),
    "Q3": ("PROMISE dataset",
           # "PROMISE" đứng một mình bị stem thành khớp cả "promising" nên chỉ dùng cụm từ
           '("PROMISE_exp" OR "PROMISE NFR" OR "PROMISE dataset" OR "PROMISE repository" OR "PROMISE corpus") '
           'AND requirements'),
    "Q4": ("Generalization / evaluation / leakage",
           '("requirements classification" OR "requirement classification") AND ("cross-project" OR '
           '"cross-domain" OR generalization OR generalisation OR leakage OR duplicate OR "cross-validation")'),
    "Q5": ("Preprocessing",
           '("requirements classification" OR "requirement classification") AND (preprocessing OR '
           '"stop words" OR stopwords OR lemmatization OR stemming OR "TF-IDF")'),
}

FIELDS = ["record_id", "openalex_id", "doi", "title", "year", "venue", "type", "authors",
          "cited_by_count", "matched_queries", "screening_decision", "reason_code", "reviewer",
          "notes", "abstract"]
MANUAL = ["screening_decision", "reason_code", "reviewer", "notes"]


def get(params, retries=4):
    url = API + "?" + urllib.parse.urlencode(params, safe=":,|*")
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as err:
            if attempt == retries - 1:
                raise
            print(f"  lỗi ({err}); thử lại sau {2 ** attempt}s", file=sys.stderr)
            time.sleep(2 ** attempt)


def abstract_of(inv):
    if not inv:
        return ""
    pos = sorted((i, w) for w, idx in inv.items() for i in idx)
    return " ".join(w for _, w in pos)


def one_line(s):
    return re.sub(r"\s+", " ", s or "").strip()


def norm_title(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def to_row(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    authors = [a["author"]["display_name"] for a in w.get("authorships", [])[:10] if a.get("author")]
    return {
        "openalex_id": w["id"].rsplit("/", 1)[-1],
        "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower(),
        "title": one_line(w.get("display_name")),
        "year": w.get("publication_year") or "",
        "venue": one_line(src.get("display_name")),
        "type": w.get("type") or "",
        "authors": "; ".join(authors),
        "cited_by_count": w.get("cited_by_count", 0),
        "abstract": one_line(abstract_of(w.get("abstract_inverted_index")))[:3000],
    }


def fetch(query, years, limit, key):
    params = {
        "filter": f"title_and_abstract.search:{query},publication_year:{years}",
        "sort": "relevance_score:desc", "per_page": min(limit, 100), "cursor": "*",
        "select": "id,doi,display_name,publication_year,primary_location,type,authorships,"
                  "cited_by_count,abstract_inverted_index",
    }
    if key:
        params["api_key"] = key
    rows, total = [], None
    while len(rows) < limit:
        data = get(params)
        total = data["meta"]["count"]
        rows += [to_row(w) for w in data["results"]]
        cursor = data["meta"].get("next_cursor")
        if not cursor or not data["results"]:
            break
        params["cursor"] = cursor
        time.sleep(0.2)
    return rows[:limit], total


def load_existing():
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def merge(existing, new_rows, qid):
    """Dedup theo OpenAlex ID → DOI → (title chuẩn hóa, year). Không xóa dòng cũ, không đụng cột sàng lọc."""
    by_id = {r["openalex_id"]: r for r in existing}
    by_doi = {r["doi"]: r for r in existing if r["doi"]}
    by_title = {(norm_title(r["title"]), str(r["year"])): r for r in existing}
    added = 0
    for n in new_rows:
        hit = (by_id.get(n["openalex_id"]) or (by_doi.get(n["doi"]) if n["doi"] else None)
               or by_title.get((norm_title(n["title"]), str(n["year"]))))
        if hit:
            qs = [q for q in hit["matched_queries"].split("|") if q]
            if qid not in qs:
                hit["matched_queries"] = "|".join(qs + [qid])
            continue
        row = {k: "" for k in FIELDS} | {k: str(v) for k, v in n.items()}
        row["record_id"] = f"R{len(existing) + 1:04d}"
        row["matched_queries"] = qid
        existing.append(row)
        by_id[row["openalex_id"]] = row
        if row["doi"]:
            by_doi[row["doi"]] = row
        by_title[(norm_title(row["title"]), str(row["year"]))] = row
        added += 1
    return added


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--queries", default=",".join(QUERIES), help="vd Q1,Q2 (mặc định: tất cả)")
    ap.add_argument("--max", type=int, default=100, help="số bản ghi tối đa mỗi query")
    ap.add_argument("--years", default="2017-2026", help="khoảng năm xuất bản, vd 2017-2026")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    sys.stderr.reconfigure(encoding="utf-8")

    key =os.environ.get("OPENALEX_API_KEY", "")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_existing()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {"runs": []}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    log_lines = [f"\n## Run {now} (harvest_openalex.py v{TOOL_VERSION})\n",
                 "| query | label | exact query (title_and_abstract.search) | years | total hits | fetched | new unique |",
                 "|---|---|---|---|---|---|---|"]

    for qid in [q.strip() for q in args.queries.split(",") if q.strip()]:
        if qid not in QUERIES:
            sys.exit(f"Không có query {qid}; chọn trong {', '.join(QUERIES)}")
        label, query = QUERIES[qid]
        print(f"{qid} {label} ...")
        got, total = fetch(query, args.years, args.max, key)
        added = merge(rows, got, qid)
        print(f"  tổng {total}, lấy {len(got)}, mới {added}")
        manifest["runs"].append({"date": now, "query_id": qid, "label": label, "query": query,
                                 "field": "title_and_abstract.search", "years": args.years,
                                 "total_hits": total, "fetched": len(got), "new_unique": added,
                                 "api_key_used": bool(key), "tool": f"harvest_openalex.py v{TOOL_VERSION}"})
        log_lines.append(f"| {qid} | {label} | `{query}` | {args.years} | {total} | {len(got)} | {added} |")

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    if not LOG_PATH.exists():
        LOG_PATH.write_text("# Search log\n\nNguồn: OpenAlex API, tìm trên title + abstract. "
                            "Bản ghi đã dedup theo OpenAlex ID → DOI → title+year.\n", encoding="utf-8")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + f"\n\nTổng số paper duy nhất sau lần chạy: {len(rows)}\n")
    print(f"Xong: {len(rows)} paper duy nhất trong {CSV_PATH.name}")


if __name__ == "__main__":
    main()
