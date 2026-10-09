#!/opt/homebrew/bin/python3
"""Grade today's Kevin posts vs medians EXCLUDING today (fair baseline)."""
import csv, statistics

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
with open(PATH) as f:
    rows = list(csv.DictReader(f))

def num(r, k):
    try:
        return float(r[k] or 0)
    except ValueError:
        return 0.0

today = [r for r in rows if r["date"] == "2026-10-09"]
print("== today's posts with full timestamps ==")
for r in sorted(today, key=lambda r: r["ts"]):
    print(f"{r['account']} {r['ts']} reel={r['is_reel']} views={num(r,'views'):.0f} likes={num(r,'likes'):.0f} comments={num(r,'comments'):.0f} er={r['er']} theme={r['theme']}")

kev_ig_prior = sorted([r for r in rows if r["account"] == "kevin_ig" and r["date"] < "2026-10-09"], key=lambda r: r["ts"])[-30:]
s = [num(r, "views") for r in kev_ig_prior if r["is_reel"] != "True" and num(r, "views") > 0]
rl = [num(r, "views") for r in kev_ig_prior if r["is_reel"] == "True" and num(r, "views") > 0]
print(f"\nkevin_ig baseline EXCL today: static median={statistics.median(s):.0f} (n={len(s)}) | reel median={statistics.median(rl):.0f} (n={len(rl)})")

kev_tt_prior = sorted([r for r in rows if r["account"] == "kevin_tt" and r["date"] < "2026-10-09"], key=lambda r: r["ts"])[-30:]
tt = [num(r, "views") for r in kev_tt_prior if num(r, "views") > 0]
print(f"kevin_tt baseline EXCL today: median={statistics.median(tt):.0f} (n={len(tt)})")

# grade
for r in today:
    v = num(r, "views")
    if r["account"] == "kevin_ig":
        base = statistics.median(s) if r["is_reel"] != "True" else statistics.median(rl)
    elif r["account"] == "kevin_tt":
        base = statistics.median(tt)
    else:
        continue
    ratio = v / base if base else 0
    verdict = "BEAT" if ratio >= 1.2 else ("MISS" if ratio < 0.8 else "AT MEDIAN")
    print(f"grade: {r['account']} reel={r['is_reel']} theme={r['theme']} {v:.0f} vs {base:.0f} = {ratio:.2f}x -> {verdict} (er={r['er']})")
