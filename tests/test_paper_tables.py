from src import paper_tables


def test_tables_built_from_results():
    rq1 = paper_tables.rq1()
    assert "\label{tab:rq1}" in rq1 and rq1.count("\\\\") >= 10
    for fn in (paper_tables.rq2, paper_tables.rq3, paper_tables.dalpiaz, paper_tables.noboth_d2,
               paper_tables.none_vs_infold, paper_tables.kendall):
        tex = fn()
        assert tex.startswith("\begin{table") and "M1" in tex
