#!/usr/bin/env python3
"""Evening brief analysis: today's posts vs medians, per-account/per-theme stats."""
import csv, statistics, datetime
from collections import defaultdict

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = []
with open(path, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def iv(r, k):
    try:
        return int(float(r[k]))
    except (ValueError, TypeError, KeyError):
        return None

TODAY = datetime.date(2026, 10, 1)
print("total rows:", len(rows), "| max date:", max(r["date"] for r in rows))

today_rows = [r for r in rows if r["date"] == "2026-10-01"]
print("posts dated 2026-10-01:", len(today_rows))

# last post + last reel per account
for acct in ["drey_ig", "drey_tt", "kevin_ig", "kevin_tt"]:
    rs = [r for r in rows if r["account"] == acct]
    last = max(rs, key=lambda r: r["ts"])
    reels = [r for r in rs if r["is_reel"] == "True"]
    last_reel = max(reels, key=lambda r: r["ts"]) if reels else None
    def days(r):
        d = datetime.date.fromisoformat(r["date"])
        return (TODAY - d).days
    print(f"{acct}: n={len(rs)} last_post={last['date']} ({days(last)}d ago, theme={last['theme']})", end="")
    if last_reel:
        print(f" | last_reel={last_reel['date']} ({days(last_reel)}d ago)")
    else:
        print(" | no reels in window")

# medians per account
print("\n-- medians per account (views) --")
by_acct = defaultdict(list)
for r in rows:
    v = iv(r, "views")
    if v is not None:
        by_acct[r["account"]].append(v)
for a in sorted(by_acct):
    print(a, "n=", len(by_acct[a]), "median=", statistics.median(by_acct[a]))

# per account+theme medians (n>=4)
print("\n-- medians per account+theme (n>=4) --")
by_theme = defaultdict(list)
for r in rows:
    v = iv(r, "views")
    if v is not None:
        by_theme[(r["account"], r["theme"])].append(v)
for k in sorted(by_theme):
    vals = by_theme[k]
    if len(vals) >= 4:
        print(k, "n=", len(vals), "median=", statistics.median(vals))

# Kevin static vs reels since 2026-09-17 (AM brief window)
print("\n-- kevin_ig static vs reel since 9/17 --")
for kind, want in (("static", "False"), ("reel", "True")):
    vals = [iv(r, "views") for r in rows
            if r["account"] == "kevin_ig" and r["is_reel"] == want
            and r["date"] >= "2026-09-17" and iv(r, "views") is not None]
    if vals:
        print(kind, "n=", len(vals), "median=", statistics.median(vals))

# Kevin recent best posts (top 5 by views since 9/17)
print("\n-- kevin_ig top since 9/17 --")
ks = [r for r in rows if r["account"] == "kevin_ig" and r["date"] >= "2026-09-17"]
for r in sorted(ks, key=lambda r: iv(r, "views") or 0, reverse=True)[:5]:
    print(r["date"], "views=", r["views"], "likes=", r["likes"], "comments=", r["comments"],
          "shares=", r["shares"], "reel=", r["is_reel"], "theme=", r["theme"])

# Drey recent posts (all since 9/1)
print("\n-- drey_ig all since 9/1 --")
ds = [r for r in rows if r["account"] == "drey_ig" and r["date"] >= "2026-09-01"]
for r in sorted(ds, key=lambda r: r["ts"]):
    print(r["date"], "views=", r["views"], "likes=", r["likes"], "comments=", r["comments"],
          "reel=", r["is_reel"], "theme=", r["theme"])
