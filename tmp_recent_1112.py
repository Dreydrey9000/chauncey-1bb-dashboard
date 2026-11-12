# Exact rows for the last 36h of founder posts (grade yesterday's PM predictions)
import csv

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = [r for r in csv.DictReader(open(path)) if r["date"] >= "2026-11-10"]
rows.sort(key=lambda r: r["ts"])
for r in rows:
    print(f"{r['account']} | ts={r['ts']} | reel={r['is_reel']} | views={r['views']} likes={r['likes']} comments={r['comments']} | theme={r['theme']}")
    print(f"   url={r['url']}")
    print(f"   caption={r['content'][:200]!r}")
