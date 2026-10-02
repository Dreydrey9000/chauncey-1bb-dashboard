# Verify Drey's August confession reels + reel-vs-static medians cited in brief
import csv, statistics

rows = [r for r in csv.DictReader(open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv", newline="", encoding="utf-8"))]
drey_ig = [r for r in rows if r["account"] == "drey_ig"]

print("--- drey_ig confession/room posts ---")
for r in sorted(drey_ig, key=lambda x: x["ts"]):
    if r["theme"] in ("confession", "room"):
        print(f"{r['date']} | reel={r['is_reel']} | theme={r['theme']} | views={r['views']} | {r['url']}")

views = [int(r["views"]) for r in drey_ig if r["is_reel"] == "True" and r["theme"] == "confession"]
print("drey_ig confession reel views:", sorted(views, reverse=True))
