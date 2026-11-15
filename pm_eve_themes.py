import csv, statistics
from collections import defaultdict

rows = list(csv.DictReader(open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv")))
for acc in ["drey_ig", "kevin_ig"]:
    themes = defaultdict(list)
    for r in rows:
        if r["account"] == acc and r["views"]:
            themes[r["theme"]].append(float(r["views"]))
    print(f"=== {acc} ALL themes ===")
    for t, vs in sorted(themes.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f"  {t}: n={len(vs)} median={statistics.median(vs):.0f}")
