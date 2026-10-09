#!/opt/homebrew/bin/python3
"""Kevin static-only median + yesterday-vs-median grading (evening 10/9)."""
import csv, statistics

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
with open(PATH) as f:
    rows = list(csv.DictReader(f))

def num(r, k):
    try:
        return float(r[k] or 0)
    except ValueError:
        return 0.0

kev_ig = sorted([r for r in rows if r["account"] == "kevin_ig"], key=lambda r: r["ts"])[-30:]
statics = [num(r, "views") for r in kev_ig if r["is_reel"] != "True" and num(r, "views") > 0]
reels = [num(r, "views") for r in kev_ig if r["is_reel"] == "True" and num(r, "views") > 0]
print(f"kevin_ig static-only median (last 30): {statistics.median(statics):.0f} (n={len(statics)})")
print(f"kevin_ig reel-only median (last 30): {statistics.median(reels):.0f} (n={len(reels)})")

kev_tt = sorted([r for r in rows if r["account"] == "kevin_tt"], key=lambda r: r["ts"])[-30:]
tt = [num(r, "views") for r in kev_tt if num(r, "views") > 0]
print(f"kevin_tt median (last 30): {statistics.median(tt):.0f} (n={len(tt)})")

drey_ig = sorted([r for r in rows if r["account"] == "drey_ig"], key=lambda r: r["ts"])[-30:]
dv = [num(r, "views") for r in drey_ig if num(r, "views") > 0]
print(f"drey_ig median (last 30): {statistics.median(dv):.0f} (n={len(dv)})")

# Kevin posting frequency last 3 days
from collections import Counter
c = Counter(r["date"] for r in rows if r["account"] in ("kevin_ig", "kevin_tt") and r["date"] >= "2026-10-06")
print("Kevin posts per day (IG+TT):", dict(sorted(c.items())))
