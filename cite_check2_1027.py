#!/opt/homebrew/bin/python3
"""Kevin static vs reel medians + Drey comment ceiling check."""
import csv, statistics

rows = [r for r in csv.DictReader(open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv", newline="", encoding="utf-8"))]
def n(r, k):
    try: return int(r[k] or 0)
    except ValueError: return 0

for acct in ["kevin_ig", "drey_ig"]:
    st = [n(r,"views") for r in rows if r["account"]==acct and r["is_reel"]=="False" and n(r,"views")>0]
    rl = [n(r,"views") for r in rows if r["account"]==acct and r["is_reel"]=="True" and n(r,"views")>0]
    print(f"{acct}: statics median={int(statistics.median(st))} (n={len(st)}) | reels median={int(statistics.median(rl))} (n={len(rl)})")

kc = [n(r,"comments") for r in rows if r["account"]=="kevin_ig" and r["is_reel"]=="False" and r["date"]>="2026-09-01" and n(r,"views")>0]
print("kevin static comments since 9/1: median", statistics.median(kc), "max", max(kc), "n", len(kc))
dc = [n(r,"comments") for r in rows if r["account"]=="drey_ig" and r["date"]>="2026-10-01" and n(r,"views")>0]
print("drey oct comments:", dc, "max", max(dc))
