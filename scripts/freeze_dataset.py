"""Đóng băng file dataset thô: ghi SHA-256 và metadata nguồn (Phase 3).

Chạy (từ gốc repo), sau khi đã copy file gốc vào data/raw/ mà KHÔNG mở/lưu lại:
    python scripts/freeze_dataset.py data/raw/PROMISE_exp.csv ^
        --name PROMISE_exp --url "<canonical URL>" --source-paper "<trích dẫn>" ^
        --version "<version/commit>" --license UNKNOWN --retrieved 2026-10-10 --expected-rows 969

Ghi data/dataset_manifest.json (danh sách file đã freeze) và data/checksums.csv.
Trường nào chưa xác minh được thì để UNKNOWN, không đoán.
Nếu file cùng đường dẫn đã freeze với hash khác, script dừng: tạo amendment và đặt tên file mới
thay vì ghi đè lịch sử.
"""

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "dataset_manifest.json"
CHECKSUMS = ROOT / "data" / "checksums.csv"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_lines(path):
    with path.open("rb") as f:
        return sum(1 for _ in f)


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    sys.stderr.reconfigure(encoding="utf-8")
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path)
    ap.add_argument("--name", required=True)
    ap.add_argument("--url", default="UNKNOWN", help="canonical URL (repo gốc, không phải mirror)")
    ap.add_argument("--doi", default="UNKNOWN")
    ap.add_argument("--source-paper", default="UNKNOWN")
    ap.add_argument("--version", default="UNKNOWN")
    ap.add_argument("--license", default="UNKNOWN")
    ap.add_argument("--retrieved", default="UNKNOWN", help="ngày tải, YYYY-MM-DD")
    ap.add_argument("--expected-rows", default="UNKNOWN", help="số dòng dữ liệu theo tài liệu nguồn")
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    path = args.file.resolve()
    if not path.is_file():
        sys.exit(f"Không thấy file {path}")
    rel = path.relative_to(ROOT).as_posix()
    digest = sha256(path)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"files": []}
    for entry in manifest["files"]:
        if entry["path"] == rel:
            if entry["sha256"] == digest:
                print(f"{rel} đã freeze, hash khớp: {digest}")
                return
            sys.exit(f"{rel} đã freeze với hash KHÁC ({entry['sha256']}).\n"
                     "File thô đã bị thay đổi hoặc đây là bản tải mới: ghi amendment và lưu dưới tên file mới.")

    entry = {
        "path": rel, "dataset_name": args.name, "sha256": digest, "size_bytes": path.stat().st_size,
        "line_count": count_lines(path), "expected_rows": args.expected_rows,
        "canonical_url": args.url, "doi": args.doi, "source_paper": args.source_paper,
        "version": args.version, "license": args.license, "retrieved_date": args.retrieved,
        "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "notes": args.notes,
    }
    manifest["files"].append(entry)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    new = not CHECKSUMS.exists()
    with CHECKSUMS.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["path", "sha256", "size_bytes", "frozen_at"])
        w.writerow([rel, digest, entry["size_bytes"], entry["frozen_at"]])

    print(f"Đã freeze {rel}\n  SHA-256 {digest}\n  {entry['line_count']} dòng vật lý (kể cả header)")
    unknown = [k for k, v in entry.items() if v == "UNKNOWN"]
    if unknown:
        print("  Còn UNKNOWN: " + ", ".join(unknown) + " (cần xác minh trước Gate G3)")
    print("Đối chiếu độc lập: Get-FileHash " + rel.replace("/", "\\") + " -Algorithm SHA256")


if __name__ == "__main__":
    main()
