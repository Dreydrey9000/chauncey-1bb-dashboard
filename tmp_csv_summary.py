#!/opt/homebrew/bin/python3
"""Summarize posts_all.csv by founder x format x theme (official Zernio data)."""
import csv, statistics, sys
from collections import defaultdict
from datetime import datetime

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = list(csv.DictReader(open(path)))

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

# newest post date per account
latest = {}
for r in rows:
    a = r["account"]
    d = r.get("date", "")
    if d and (a not in latest or d > latest[a]):
        latest[a] = d

buckets = defaultdict(list)
themes = defaultdict(lambda: defaultdict(list))
for r in rows:
    who = "DREY" if r["account"].startswith("drey") else ("KEVIN" if r["account"].startswith("kevin") else None)
    if not who:
        continue
    v = num(r.get("views"))
    fmt = ("reel" if r.get("is_reel", "").strip().lower() in ("1", "true") else "static")
    if v is not None:
        buckets[(who, fmt)].append(v)
        t = (r.get("theme") or "none").strip() or "none"
        themes[(who, fmt)][t].append(v)

print("=== coverage ===")
for a in sorted(latest):
    print(f"{a}: latest post {latest[a]}")

print("\n=== views by founder x format (n, median, mean, max) ===")
for k in sorted(buckets):
    vals = buckets[k]
    print(f"{k}: n={len(vals)} median={statistics.median(vals):.0f} mean={statistics.mean(vals):.0f} max={max(vals):.0f}")

print("\n=== DREY reels by theme (n, median, top post) ===")
for t, vals in sorted(themes.get(("DREY", "reel"), {}).items(), key=lambda x: -statistics.median(x[1])):
    print(f"  {t}: n={len(vals)} median={statistics.median(vals):.0f} max={max(vals):.0f}")

print("\n=== KEVIN reels by theme (n, median, top post) ===")
for t, vals in sorted(themes.get(("KEVIN", "reel"), {}).items(), key=lambda x: -statistics.median(x[1])):
    print(f"  {t}: n={len(vals)} median={statistics.median(vals):.0f} max={max(vals):.0f}")

print("\n=== last 6 posts per founder (date, fmt, views, theme, first 60 chars) ===")
for who in ("DREY", "KEVIN"):
    sub = [r for r in rows if r["account"].startswith(who.lower())]
    sub.sort(key=lambda r: r.get("ts", ""), reverse=True)
    print(f"--- {who} ---")
    for r in sub[:6]:
        print(f"  {r['date']} {'reel' if r['is_reel'].strip().lower() in ('1','true') else 'stat'} v={r['views']} {r['theme']}: {r['content'][:60].replace(chr(10),' ')}")
