#!/usr/bin/env python3
"""PM inspire-brief prep: today's founder posts + per-account medians (feed posts only).
Reads dashboard/posts_all.csv (6:31a snapshot). Prints exact medians via repr().
"""
import csv, statistics, re
from collections import defaultdict

CSV = "posts_all.csv"
TODAY = "2026-11-27"

with open(CSV, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print("total rows:", len(rows))

def num(r, k):
    try:
        return float(r[k])
    except (ValueError, TypeError, KeyError):
        return None

def is_feed(r):
    u = r.get("url") or ""
    return ("/stories/" not in u) and bool((r.get("content") or "").strip())

todays = [r for r in rows if r.get("date") == TODAY]
print("posts dated", TODAY, ":", len(todays))
for r in todays:
    print("TODAY |", r["account"], "|", r["ts"], "|", r["url"], "| views", r["views"],
          "| likes", r["likes"], "| comments", r["comments"], "| saves", r["saves"],
          "| shares", r["shares"], "| reel", r["is_reel"], "|", r["theme"])

latest = {}
for r in rows:
    a = r["account"]
    if a not in latest or r["date"] > latest[a]:
        latest[a] = r["date"]
print("latest post date per account:", dict(sorted(latest.items())))

wk = [r for r in rows if "2026-11-20" <= r["date"] <= TODAY]
print("feed posts last 7 days (11-20..27):", sum(1 for r in wk if is_feed(r)))
for r in wk:
    if is_feed(r):
        print("WK |", r["date"], "|", r["account"], "|", (r["url"] or "")[-28:], "| views", r["views"], "|", r["theme"])

# medians by account: feed posts, last 90 days of data (2026-08-29..11-27), views>0 known
groups = defaultdict(list)
for r in rows:
    if is_feed(r):
        v = num(r, "views")
        if v is not None and v > 0:
            groups[r["account"]].append(v)

print("\nmedians (all feed posts with views, exact):")
for a in sorted(groups):
    x = sorted(groups[a])
    print(f"  {a}: n={len(x)} median={statistics.median(x)!r} max={max(x)!r}")

# is_reel split for founders
print("\nreel vs static medians (feed, views>0):")
for a in sorted(groups):
    reel_v = [num(r, "views") for r in rows if r["account"] == a and is_feed(r) and r.get("is_reel") == "True"]
    stat_v = [num(r, "views") for r in rows if r["account"] == a and is_feed(r) and r.get("is_reel") == "False"]
    reel_v = [v for v in reel_v if v and v > 0]
    stat_v = [v for v in stat_v if v and v > 0]
    if reel_v:
        print(f"  {a} reels: n={len(reel_v)} median={statistics.median(reel_v)!r}")
    if stat_v:
        print(f"  {a} statics: n={len(stat_v)} median={statistics.median(stat_v)!r}")

# theme medians for founders (feed, views>0)
print("\ntheme medians (feed, views>0, n>=5):")
tg = defaultdict(list)
for r in rows:
    if is_feed(r) and r["account"] in ("drey_ig", "drey_tt", "kevin_ig"):
        v = num(r, "views")
        if v and v > 0:
            tg[(r["account"], r["theme"])].append(v)
for (a, t), x in sorted(tg.items()):
    if len(x) >= 5:
        print(f"  {a} {t}: n={len(x)} median={statistics.median(x)!r}")

# caption of today's posts (full, for slogan/format checks)
print("\nfull captions of today's posts:")
for r in todays:
    print("CAPTION", r["account"], r["url"])
    print((r.get("content") or "")[:600])
    print("---")
