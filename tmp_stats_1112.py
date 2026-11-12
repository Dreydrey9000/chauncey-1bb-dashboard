# Own-data anchors from posts_all.csv for the 2026-11-12 AM inspire brief
import csv, statistics as st
from collections import defaultdict

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = list(csv.DictReader(open(path)))
print("total rows:", len(rows))

recent = [r for r in rows if "2026-09-14" <= r["date"] <= "2026-11-12"]
print("rows since 2026-09-14:", len(recent))

def views(r):
    try:
        return int(float(r["views"]))
    except Exception:
        return None

for founder in ["drey_ig", "kevin_ig"]:
    fr = [r for r in recent if r["account"] == founder and views(r) is not None]
    if not fr:
        print(founder, "NO DATA")
        continue
    v = [views(r) for r in fr]
    print(f"\n== {founder}: n={len(fr)} median_views={int(st.median(v))} max={max(v)}")
    bytheme = defaultdict(list)
    for r in fr:
        bytheme[r["theme"]].append(views(r))
    for t, vs in sorted(bytheme.items(), key=lambda kv: -st.median(kv[1])):
        print(f"   {t}: n={len(vs)} median={int(st.median(vs))} max={max(vs)}")
    reels = [views(r) for r in fr if r["is_reel"] == "True"]
    statics = [views(r) for r in fr if r["is_reel"] != "True"]
    if reels and statics:
        print(f"   reels n={len(reels)} median={int(st.median(reels))} | static n={len(statics)} median={int(st.median(statics))}")
    fr.sort(key=lambda r: r["ts"])
    for r in fr[-4:]:
        print(f"   LAST {r['date']} {r['theme']} reel={r['is_reel']} views={r['views']} comments={r['comments']} :: {r['content'][:70]}")
