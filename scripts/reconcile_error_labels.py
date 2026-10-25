"""Ghép nhãn error analysis của Phát Tài và Hoàng Anh (protocol §11). Chạy từ thư mục gốc repo:
    python scripts/reconcile_error_labels.py merge   -> tạo results/predictions/error_analysis_reconciled.csv + in mức đồng thuận
    python scripts/reconcile_error_labels.py counts  -> kiểm tra reconciled_category và in bảng đếm cho paper
"""
import sys
import pandas as pd

P = "results/predictions/"
CATS = ["mixed FR/NFR", "quality keyword in FR", "functional verb in NFR", "ambiguous/underspecified",
        "short/low context", "possible annotation issue", "other"]
OUT = P + "error_analysis_reconciled.csv"


def kappa(a, b):
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in CATS)
    return (po - pe) / (1 - pe)


def merge():
    pt = pd.read_csv(P + "error_analysis_phat_tai_completed.csv", keep_default_na=False, dtype=str)
    ha = pd.read_csv(P + "error_analysis_hoang_anh_completed.csv", keep_default_na=False, dtype=str)
    for name, d, col in (("Phat Tai", pt, "phat_tai_category"), ("Hoang Anh", ha, "hoang_anh_category")):
        bad = sorted(set(d[col]) - set(CATS))
        assert len(d) == 30 and d.row_id.nunique() == 30, f"{name}: can 30 dong, 30 row_id"
        assert not bad, f"{name}: nhan khong hop le {bad}"
    m = pt.drop(columns="hoang_anh_category").merge(ha[["row_id", "hoang_anh_category"]], on="row_id", validate="1:1")
    m = m[pt.columns]  # giữ thứ tự cột gốc
    same = m.phat_tai_category == m.hoang_anh_category
    m.loc[same, "reconciled_category"] = m.loc[same, "phat_tai_category"]
    m.to_csv(OUT, index=False, encoding="utf-8")
    print(f"Dong y: {same.sum()}/30 ({same.mean():.0%}); Cohen's kappa = {kappa(m.phat_tai_category, m.hoang_anh_category):.3f}")
    print(f"Can thao luan {(~same).sum()} dong (reconciled_category dang trong):")
    print(m.loc[~same, ["row_id", "model", "true_label", "phat_tai_category", "hoang_anh_category", "text"]].to_string(index=False))
    print(f"Da ghi {OUT}")


def counts():
    m = pd.read_csv(OUT, keep_default_na=False, dtype=str)
    bad = sorted(set(m.reconciled_category) - set(CATS))
    assert not bad, f"reconciled_category con trong/khong hop le: {bad}"
    changed = m.reconciled_category.ne(m.phat_tai_category) | m.reconciled_category.ne(m.hoang_anh_category)
    assert m.loc[changed, "note"].ne("").all(), "Dong bat dong nao cung phai co note"
    t = pd.crosstab(m.reconciled_category, m.true_label).reindex(CATS, fill_value=0)
    t["M2"] = m[m.model == "M2"].reconciled_category.value_counts().reindex(CATS, fill_value=0)
    t["M5"] = m[m.model == "M5"].reconciled_category.value_counts().reindex(CATS, fill_value=0)
    t["Total"] = t.M2 + t.M5
    print(t.sort_values("Total", ascending=False).to_string())
    print("Tong:", t.Total.sum())


{"merge": merge, "counts": counts}[sys.argv[1]]()
