# Evening delta analysis: today's founder posts vs medians (reads posts_all.csv, prints only)
import csv, statistics
from collections import defaultdict

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
TODAY = "2026-10-02"

rows = []
with open(PATH, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append(r)

print("total rows:", len(rows))
dates = sorted(r["date"] for r in rows if r["date"])
print("date range:", dates[0], "->", dates[-1])

todays = [r for r in rows if r["date"] == TODAY]
print(f"\n--- posts dated {TODAY}: {len(todays)} ---")
for r in sorted(todays, key=lambda x: x["ts"]):
    print(f"{r['account']} | {r['ts']} | reel={r['is_reel']} | theme={r['theme']} | views={r['views']} likes={r['likes']} comments={r['comments']} saves={r['saves']} shares={r['shares']} er={r['er']}")
    print(f"   {r['url']}")
    print(f"   {r['content'][:140].replace(chr(10), ' ')}")

# Medians: per founder+platform, reel vs static, all-time AND since 9/2 (recent era used in prior briefs)
def med(vals):
    vals = [int(v) for v in vals if str(v).strip() not in ("", "None")]
    return statistics.median(vals) if vals else None

groups = defaultdict(list)
for r in rows:
    fmt = "reel" if r["is_reel"] == "True" else "static"
    era = "recent" if r["date"] >= "2026-09-02" else "all"
    groups[(r["account"], fmt, era)].append(r)

print("\n--- medians views by account/format/era ---")
for k in sorted(groups):
    g = groups[k]
    v = med([x["views"] for x in g])
    c = med([x["comments"] for x in g])
    print(f"{k} n={len(g)} median_views={v} median_comments={c}")

print("\n--- posts since 2026-09-29 (recency context) ---")
recent = [r for r in rows if r["date"] >= "2026-09-29"]
for r in sorted(recent, key=lambda x: x["ts"]):
    print(f"{r['account']} | {r['date']} | reel={r['is_reel']} | theme={r['theme']} | views={r['views']} comments={r['comments']} | {r['url']}")
