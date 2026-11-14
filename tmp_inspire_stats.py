# Morning inspire brief stats — founder lanes from posts_all.csv ( Chauncey, cron-safe file run )
import csv, statistics
from collections import defaultdict
from datetime import date, timedelta

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = list(csv.DictReader(open(PATH)))

def to_int(v):
    try:
        return int(float(v))
    except Exception:
        return None

for r in rows:
    r["v"] = to_int(r.get("views"))
    r["c"] = to_int(r.get("comments"))
    r["l"] = to_int(r.get("likes"))

maxd = max(r["date"] for r in rows if r.get("date"))
print("CSV max date:", maxd, "| total rows:", len(rows))

md = date.fromisoformat(maxd)
cut7 = (md - timedelta(days=7)).isoformat()

for acct in ["drey_ig", "kevin_ig"]:
    sub = sorted([r for r in rows if r["account"] == acct and r["date"] >= cut7], key=lambda r: r["ts"])
    print(f"\n=== {acct} last 7d ({len(sub)} posts) ===")
    for r in sub:
        v = r["v"] if r["v"] is not None else "n/a"
        print(f"{r['date']} {r['ts'][11:16]}UTC v={v} c={r['c']} l={r['l']} reel={r['is_reel']} theme={r['theme']} :: {r['content'][:70].replace(chr(10),' ')}")

for acct in ["drey_ig", "kevin_ig"]:
    themes = defaultdict(list)
    for r in rows:
        if r["account"] == acct and r["v"] is not None:
            themes[r["theme"]].append(r["v"])
    print(f"\n=== {acct} theme medians all-time (n>=4) ===")
    for t, vals in sorted(themes.items(), key=lambda kv: -statistics.median(kv[1])):
        if len(vals) >= 4:
            print(f"{t:12} n={len(vals):>3} median={statistics.median(vals):>7.0f}")
    allv = [r["v"] for r in rows if r["account"] == acct and r["v"] is not None]
    reels = [r["v"] for r in rows if r["account"] == acct and r["is_reel"] == "True" and r["v"] is not None]
    statics = [r["v"] for r in rows if r["account"] == acct and r["is_reel"] == "False" and r["v"] is not None]
    print(f"account median={statistics.median(allv):.0f} (n={len(allv)}) | reels median={statistics.median(reels):.0f} (n={len(reels)}) | statics median={statistics.median(statics):.0f} (n={len(statics)})")

# completion rate proxy for kevin reels (watch_ms & dur_s present sometimes)
kr = [r for r in rows if r["account"] == "kevin_ig" and r["is_reel"] == "True" and r.get("dur_s") not in ("", None) and r.get("watch_ms") not in ("", None)]
if kr:
    rates = []
    for r in kr:
        try:
            rates.append(100.0 * (float(r["watch_ms"]) / 1000.0) / float(r["dur_s"]))
        except Exception:
            pass
    if rates:
        rates.sort()
        print(f"\nkevin_ig reel completion rates (n={len(rates)}): median={statistics.median(rates):.1f}% min={rates[0]:.1f}% max={rates[-1]:.1f}%")
