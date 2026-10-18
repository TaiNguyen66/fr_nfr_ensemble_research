from src import paper_tables


def test_tables_built_from_results():
    rq1 = paper_tables.rq1()
    assert r"\label{tab:rq1}" in rq1 and rq1.count(r" \\") == 9  # 2 header lines + M0..M6
    for fn in (paper_tables.rq2, paper_tables.rq3, paper_tables.dalpiaz, paper_tables.noboth_d2,
               paper_tables.none_vs_infold, paper_tables.kendall):
        tex = fn()
        assert tex.startswith(r"\begin{table") and "M1" in tex
