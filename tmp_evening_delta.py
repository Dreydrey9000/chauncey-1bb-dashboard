# Evening delta: today's founder posts vs medians
import csv, statistics as st
from collections import defaultdict

CSV = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
TODAY = "2026-10-07"

rows = []
with open(CSV, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rows.append(r)

def clean(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

# Today's posts per account
print(f"=== Posts dated {TODAY} ===")
todays = [r for r in rows if r["date"] == TODAY]
if not todays:
    print("NONE")
for r in todays:
    print(f"{r['account']} | {r['theme']} | reel={r['is_reel']} | views={r['views']} "
          f"| likes={r['likes']} | comments={r['comments']} | saves={r['saves']} "
          f"| shares={r['shares']} | er={r['er']} | {r['url']}")
    print(f"   caption: {r['content'][:180]}")

# Latest post date per account (staleness check)
print("\n=== Latest post per account ===")
latest = {}
for r in rows:
    a = r["account"]
    if a not in latest or r["date"] > latest[a]["date"]:
        latest[a] = r
for a, r in sorted(latest.items()):
    print(f"{a}: last post {r['date']} ({r['theme']}, views={r['views']})")

# Medians per founder (IG only for the IG median context; and all)
print("\n=== Medians (views) ===")
groups = defaultdict(list)
for r in rows:
    v = clean(r["views"])
    if v is None:
        continue
    groups[r["account"]].append((v, r["theme"], r["is_reel"]))
for a in sorted(groups):
    vals = [v for v, _, _ in groups[a]]
    reels = [v for v, _, ir in groups[a] if ir == "True"]
    statics = [v for v, _, ir in groups[a] if ir != "True"]
    themes = defaultdict(list)
    for v, t, _ in groups[a]:
        themes[t].append(v)
    theme_str = ", ".join(f"{t}: n={len(vs)} med={int(st.median(vs))}" for t, vs in sorted(themes.items(), key=lambda kv: -st.median(kv[1]))[:5])
    print(f"{a}: n={len(vals)} median={int(st.median(vals))} | reels n={len(reels)} med={int(st.median(reels)) if reels else '-'} | static n={len(statics)} med={int(st.median(statics)) if statics else '-'}")
    print(f"   themes: {theme_str}")

# If today has posts, compare vs that account median
print("\n=== Today vs median ===")
for r in todays:
    a = r["account"]
    vals = [clean(x["views"]) for x in rows if x["account"] == a and clean(x["views"]) is not None]
    med = st.median(vals)
    v = clean(r["views"])
    if v is not None and med:
        ratio = v / med
        print(f"{a}: {int(v)} views vs median {int(med)} -> {ratio:.2f}x ({'BEAT' if ratio >= 1.3 else 'miss' if ratio < 0.7 else 'in line'})")
