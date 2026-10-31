#!/usr/bin/env python3
"""Evening inspire: compute 7-day medians by account + post type from posts_all.csv."""
import csv, statistics, datetime

BASE = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard"
cutoff = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()

rows = []
with open(f"{BASE}/posts_all.csv", newline="") as f:
    for r in csv.DictReader(f):
        rows.append(r)

print(f"CSV rows: {len(rows)}, 7d cutoff: {cutoff}")

def med(prefix, label, reel_filter=None):
    vals = []
    for r in rows:
        if r["account"] != prefix:
            continue
        if not r["date"] or r["date"] < cutoff:
            continue
        is_reel = r.get("is_reel", "")
        if reel_filter is True and is_reel.strip().lower() not in ("1", "true", "yes"):
            continue
        if reel_filter is False and is_reel.strip().lower() in ("1", "true", "yes"):
            continue
        try:
            v = int(float(r["views"] or 0))
        except ValueError:
            continue
        vals.append(v)
    if vals:
        print(f"{prefix} {label} 7d: n={len(vals)} median={statistics.median(vals)} values={sorted(vals)}")
    else:
        print(f"{prefix} {label} 7d: n=0")

for acct in ("drey_ig", "drey_tt", "kevin_ig", "kevin_tt"):
    med(acct, "reels", True)
    med(acct, "statics", False)
    med(acct, "all", None)
