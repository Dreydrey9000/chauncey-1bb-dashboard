#!/opt/homebrew/bin/python3
"""Evening delta 2026-10-09: founders' posts from today vs their medians."""
import csv, statistics, json

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
with open(PATH) as f:
    rows = list(csv.DictReader(f))

def num(r, k):
    try:
        return float(r[k] or 0)
    except ValueError:
        return 0.0

# Today's posts
today = [r for r in rows if r["date"] == "2026-10-09"]
yesterday = [r for r in rows if r["date"] in ("2026-10-08", "2026-10-07")]
print("TODAY 2026-10-09 posts:", len(today))
for r in today:
    print(json.dumps({
        "account": r["account"], "url": r["url"], "views": r["views"],
        "reach": r["reach"], "likes": r["likes"], "comments": r["comments"],
        "shares": r["shares"], "saves": r["saves"], "er": r["er"],
        "is_reel": r["is_reel"], "theme": r["theme"],
        "content": (r["content"] or "")[:80],
    }))

# Latest post date per account
latest = {}
for r in rows:
    a = r["account"]
    if a not in latest or r["date"] > latest[a]:
        latest[a] = r["date"]
print("\nLatest date per account:", json.dumps(latest, sort_keys=True))

# Medians: last 30 posts per account by views (and reels-only median where useful)
print("\n=== Per-account medians (last 30 posts) ===")
for acct in sorted(set(r["account"] for r in rows)):
    sub = sorted([r for r in rows if r["account"] == acct], key=lambda r: r["ts"])[-30:]
    views = [num(r, "views") for r in sub if num(r, "views") > 0]
    reels = [num(r, "views") for r in sub if r["is_reel"] == "True" and num(r, "views") > 0]
    if views:
        line = f"{acct}: n={len(sub)} median_views={statistics.median(views):.0f}"
        if reels:
            line += f" | reels-only median={statistics.median(reels):.0f} (n={len(reels)})"
        print(line)

# Theme medians for recent Drey IG reels and Kevin IG (context for tweak)
print("\n=== Drey IG reels by theme (last 40 drey_ig reels) ===")
drey_reels = sorted([r for r in rows if r["account"] == "drey_ig" and r["is_reel"] == "True"], key=lambda r: r["ts"])[-40:]
themes = {}
for r in drey_reels:
    themes.setdefault(r["theme"], []).append(num(r, "views"))
for t, v in sorted(themes.items(), key=lambda kv: -statistics.median(kv[1]) if kv[1] else 0):
    if v:
        print(f"  {t}: n={len(v)} median={statistics.median(v):.0f} max={max(v):.0f}")

print("\n=== Kevin IG by theme (last 40 kevin_ig posts) ===")
kev = sorted([r for r in rows if r["account"] == "kevin_ig"], key=lambda r: r["ts"])[-40:]
kthemes = {}
for r in kev:
    kthemes.setdefault(r["theme"], []).append(num(r, "views"))
for t, v in sorted(kthemes.items(), key=lambda kv: -statistics.median(kv[1]) if kv[1] else 0):
    if v:
        print(f"  {t}: n={len(v)} median={statistics.median(v):.0f} max={max(v):.0f}")

# Yesterday-ish posts detail for the delta (most recent 6 per founder)
print("\n=== Most recent 6 posts per founder account ===")
for acct in ("drey_ig", "drey_tt", "kevin_ig", "kevin_tt"):
    sub = sorted([r for r in rows if r["account"] == acct], key=lambda r: r["ts"])[-6:]
    print(f"-- {acct}")
    for r in sub:
        print(f"  {r['date']} reel={r['is_reel']} views={r['views']} likes={r['likes']} comments={r['comments']} er={r['er']} theme={r['theme']} | {(r['content'] or '')[:60]}")
