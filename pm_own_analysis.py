#!/usr/bin/env python3
"""Evening inspire brief: own-data analysis from posts_all.csv (read-only)."""
import csv, statistics, json
from collections import defaultdict

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
TODAY = "2026-11-10"

rows = []
with open(PATH, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows.append(row)

print("total rows:", len(rows))
dates = sorted(set(r["date"] for r in rows))
print("date range:", dates[0], "->", dates[-1])

def med(vals):
    vals = [float(v) for v in vals if v not in ("", None)]
    return statistics.median(vals) if vals else None

by_acct = defaultdict(list)
for r in rows:
    by_acct[r["account"]].append(r)

print("\n== Medians (views) by account ==")
for acct in sorted(by_acct):
    rs = sorted(by_acct[acct], key=lambda x: x["ts"])
    ig = [r for r in rs if acct.endswith("_ig")]
    all_med = med([r["views"] for r in rs])
    last30_med = med([r["views"] for r in rs[-30:]])
    print(f"{acct}: n={len(rs)} alltime={all_med:.0f} last30={last30_med:.0f} latest={max(r['date'] for r in rs)}")

print(f"\n== Posts dated {TODAY} (CSV snapshot) ==")
todays = [r for r in rows if r["date"] == TODAY]
print("count:", len(todays))
for r in todays:
    print(json.dumps({k: r[k] for k in ["account","ts","url","views","likes","comments","is_reel","theme"]}, ensure_ascii=False))
    print("  caption:", r["content"][:120].replace("\n", " / "))

print("\n== Last 5 posts per founder account (context for medians) ==")
for acct in sorted(by_acct):
    rs = sorted(by_acct[acct], key=lambda x: x["ts"])[-5:]
    print(f"-- {acct}")
    for r in rs:
        print(f"  {r['date']} views={r['views']:>7} likes={r['likes']:>4} cmts={r['comments']:>3} reel={r['is_reel']} theme={r['theme']} | {r['content'][:60].strip()}")
