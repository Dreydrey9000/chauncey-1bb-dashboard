# Compute founder stats from posts_all.csv for the inspire brief (chauncey cron)
import csv, statistics, collections

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = []
with open(path) as f:
    for r in csv.DictReader(f):
        try:
            r["views_i"] = int(r["views"]) if r["views"] else None
        except ValueError:
            r["views_i"] = None
        rows.append(r)

def med(vals):
    vals = [v for v in vals if v is not None]
    return round(statistics.median(vals)) if vals else None

print("== median views by founder/theme (n>=3) ==")
agg = collections.defaultdict(list)
for r in rows:
    who = r["account"].split("_")[0]
    if r["views_i"] is not None:
        agg[(who, r["theme"])].append(r["views_i"])
for (who, theme), vals in sorted(agg.items()):
    if len(vals) >= 3:
        print(f"{who:6s} {theme:12s} n={len(vals):3d} median={med(vals)}")

print("\n== reel vs static median views per founder ==")
for who in ("drey", "kevin"):
    for is_reel in ("True", "False"):
        vals = [r["views_i"] for r in rows if r["account"].startswith(who) and r["is_reel"] == is_reel and r["views_i"]]
        print(f"{who} reel={is_reel}: n={len(vals)} median={med(vals)}")

print("\n== posts since 2026-09-23 (last 7 days) ==")
recent = sorted([r for r in rows if r["date"] >= "2026-09-23"], key=lambda r: (r["date"], r["account"]))
for r in recent:
    print(f"{r['date']} {r['account']:9s} v={r['views_i']} likes={r['likes']} com={r['comments']} shares={r['shares']} saves={r['saves']} reel={r['is_reel']} theme={r['theme']}")
    print(f"   cap: {r['content'][:100].replace(chr(10),' ')}")
    print(f"   url: {r['url']}")

print("\n== latest 3 posts per founder ==")
for who in ("drey", "kevin"):
    sub = sorted([r for r in rows if r["account"].startswith(who)], key=lambda r: r["date"], reverse=True)[:3]
    for r in sub:
        print(f"{who}: {r['date']} v={r['views_i']} reel={r['is_reel']} theme={r['theme']} url={r['url'][:70]}")

print("\n== overall date range ==")
dates = sorted(r["date"] for r in rows if r["date"])
print(f"{dates[0]} .. {dates[-1]}  total_rows={len(rows)}")
