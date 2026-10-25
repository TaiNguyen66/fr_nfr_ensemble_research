import re

from src import paper_tables


def test_tables_built_from_results():
    rq1 = paper_tables.rq1()
    assert r"\label{tab:rq1}" in rq1 and rq1.count(r" \\") == 9  # 2 header lines + M0..M6
    for fn in (paper_tables.rq2, paper_tables.rq3, paper_tables.dalpiaz, paper_tables.noboth_d2,
               paper_tables.none_vs_infold, paper_tables.kendall):
        tex = fn()
        assert tex.startswith(r"\begin{table") and "M1" in tex


def test_none_vs_infold_fits_one_column():
    tex = paper_tables.none_vs_infold()
    assert tex.startswith(r"\begin{table}[t]") and r"\begin{tabular}{l c cr cr}" in tex
    assert "T-bin (FR vs NFR)" in tex and "T-12 (12 classes)" in tex
    assert sum(bool(re.match(r"M\d &", line)) for line in tex.splitlines()) == 10  # M1..M5 in each panel
