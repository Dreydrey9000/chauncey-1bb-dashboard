#!/usr/bin/env python3
"""Morning brief CSV stats: recent-window + theme medians for grounding."""
import csv, statistics
from collections import defaultdict
from datetime import datetime, timedelta

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"

def to_int(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None

rows = []
with open(PATH) as f:
    for r in csv.DictReader(f):
        try:
            r["_date"] = datetime.strptime(r["date"], "%Y-%m-%d")
        except ValueError:
            continue
        rows.append(r)

rows.sort(key=lambda r: r["_date"], reverse=True)
latest = max(r["_date"] for r in rows)
print("LATEST POST DATE IN CSV:", latest.date())

cutoff = latest - timedelta(days=14)
recent = [r for r in rows if r["_date"] >= cutoff]

def summarize(subset, label):
    views = [to_int(r["views"]) for r in subset if to_int(r["views"]) is not None]
    if not views:
        print(f"{label}: no data")
        return
    print(f"{label}: n={len(views)} median_views={statistics.median(views):.0f} max={max(views)}")

summarize(recent, "ALL recent-14d")

for acct in ["drey_ig", "drey_tt", "kevin_ig", "kevin_tt"]:
    sub = [r for r in recent if r["account"] == acct]
    summarize(sub, acct)
    sub_sorted = sorted([r for r in sub if to_int(r["views"]) is not None],
                        key=lambda r: to_int(r["views"]), reverse=True)
    for r in sub_sorted[:3]:
        c = " ".join(r["content"].split())[:90]
        print(f"   {r['date']} [{r['theme']}] views={r['views']} comments={r['comments']} likes={r['likes']} reel={r['is_reel']} :: {c}")

print("\nTHEME MEDIANS (full history, IG views):")
for acct in ["drey_ig", "kevin_ig"]:
    themes = defaultdict(list)
    for r in rows:
        if r["account"] == acct and to_int(r["views"]) is not None:
            themes[r["theme"]].append(to_int(r["views"]))
    tstat = sorted(((t, len(v), statistics.median(v)) for t, v in themes.items() if len(v) >= 2),
                   key=lambda x: -x[2])
    for t, n, m in tstat:
        print(f"  {acct} {t}: n={n} median={m:.0f}")

allv = [to_int(r["views"]) for r in rows if to_int(r["views"]) is not None]
print(f"\nALL-TIME median views across all posts: {statistics.median(allv):.0f}")
