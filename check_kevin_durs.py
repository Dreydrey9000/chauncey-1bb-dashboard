# Kevin recent reels with durations + Drey reel silence check
import csv

rows = [r for r in csv.DictReader(open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv", newline="", encoding="utf-8"))]

print("--- kevin_ig reels since 9/15 (views, duration) ---")
for r in sorted([x for x in rows if x["account"] == "kevin_ig" and x["is_reel"] == "True" and x["date"] >= "2026-09-15"], key=lambda x: x["ts"]):
    print(f"{r['date']} {r['ts'][11:16]}UTC | dur={r['dur_s']}s | views={r['views']} | theme={r['theme']} | {r['url'][:60]}")
