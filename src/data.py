"""Load the frozen datasets into one tidy table (protocol §4, A-007).

Columns: requirement_id, text, label_12, label_bin, project_id.
Text is returned as in the raw file; P0 preprocessing (§5) is applied by the model pipeline.
"""
import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROMISE_PATH = ROOT / "data/raw/PROMISE_exp.arff"
DALPIAZ_DIR = ROOT / "data/raw/dalpiaz2019"
DALPIAZ_SETS = ("dronology", "leeds", "reqview", "wasp")

_ROW = re.compile(r"^\s*([^,]+?)\s*,\s*(['\"])(.*)\2\s*,\s*([A-Za-z]+)\s*$")


def load_promise_exp(path=PROMISE_PATH):
    raw = Path(path).read_text(encoding="utf-8")
    body = raw[raw.lower().index("@data") + len("@data"):]
    rows = []
    for line in body.splitlines():
        if not line.strip() or line.lstrip().startswith("%"):
            continue
        m = _ROW.match(line)
        if not m:
            raise ValueError(f"Unparsable ARFF row: {line[:80]!r}")
        rows.append((m.group(1), m.group(3).replace("\'", "'"), m.group(4)))
    df = pd.DataFrame(rows, columns=["project_id", "text", "label_12"])
    df.insert(0, "requirement_id", [f"P{i:04d}" for i in range(len(df))])
    df["label_bin"] = (df["label_12"] == "F").map({True: "FR", False: "NFR"})
    return df[["requirement_id", "text", "label_12", "label_bin", "project_id"]]


def load_dalpiaz(directory=DALPIAZ_DIR, drop_both=False):
    """Four public Dalpiaz et al. (2019) sets; dataset name is the project id.

    IsQuality = 1 -> NFR (also when IsFunctional = 1); IsFunctional only -> FR; no label -> dropped.
    drop_both=True is the sensitivity analysis that removes rows carrying both labels.
    """
    parts = []
    for name in DALPIAZ_SETS:
        d = pd.read_csv(Path(directory) / f"{name}.csv")
        d = d[(d.IsFunctional == 1) | (d.IsQuality == 1)]
        if drop_both:
            d = d[~((d.IsFunctional == 1) & (d.IsQuality == 1))]
        parts.append(pd.DataFrame({
            "text": d.RequirementText.astype(str).values,
            "label_12": None,
            "label_bin": (d.IsQuality == 1).map({True: "NFR", False: "FR"}).values,
            "project_id": name,
        }))
    df = pd.concat(parts, ignore_index=True)
    df.insert(0, "requirement_id", [f"D{i:04d}" for i in range(len(df))])
    return df


def canonical(text):
    """Canonical form for duplicate grouping (§4.2 step 1)."""
    s = unicodedata.normalize("NFKC", text).lower().strip()
    s = re.sub(r"\s+", " ", s)
    return re.sub(r"[\s.;:,!?]+$", "", s)


def preprocess_p0(text):
    """P0 (§5): NFKC, lowercase, expand negative contractions, collapse whitespace."""
    s = unicodedata.normalize("NFKC", text).lower()
    s = s.replace("won't", "will not").replace("can't", "cannot").replace("n't", " not")
    return re.sub(r"\s+", " ", s).strip()
