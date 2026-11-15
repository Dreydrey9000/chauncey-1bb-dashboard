import csv, statistics, json
from collections import defaultdict

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = list(csv.DictReader(open(path)))
print("total rows:", len(rows))

TODAY = "2026-11-15"
today_rows = [r for r in rows if r["date"] == TODAY]
print(f"--- posts dated {TODAY}: {len(today_rows)} ---")
for r in today_rows:
    print(r["account"], "| views:", r["views"], "| likes:", r["likes"], "| comments:", r["comments"], "| reel:", r["is_reel"], "| theme:", r["theme"], "|", r["url"])
    print("   text:", (r["content"] or "")[:150].replace("\n", " "))

print("\n--- last 6 rows by ts ---")
for r in sorted(rows, key=lambda r: r["ts"] or "")[-6:]:
    print(r["account"], "|", r["date"], "| views:", r["views"], "|", (r["url"] or "")[:70])

def med(vals):
    vals = [float(v) for v in vals if v not in ("", None)]
    return statistics.median(vals) if vals else None

accs = defaultdict(list)
for r in rows:
    accs[r["account"]].append(r)

for acc in ["drey_ig", "kevin_ig"]:
    rs = accs[acc]
    reels = [r for r in rs if r["is_reel"] == "True"]
    statics = [r for r in rs if r["is_reel"] != "True"]
    print(f"\n{acc}: n={len(rs)} | median views ALL={med([r['views'] for r in rs]):.0f} | reels n={len(reels)} med={med([r['views'] for r in reels])} | static n={len(statics)} med={med([r['views'] for r in statics])}")
    themes = defaultdict(list)
    for r in rs:
        if r["views"]:
            themes[r["theme"]].append(float(r["views"]))
    tm = [(t, len(vs), med(vs)) for t, vs in themes.items() if len(vs) >= 3]
    for t, n, m in sorted(tm, key=lambda x: -(x[2] or 0)):
        print(f"  theme {t}: n={n} median={m:.0f}")
