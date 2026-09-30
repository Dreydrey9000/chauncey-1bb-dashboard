#!/usr/bin/env python3
"""Evening delta analysis for inspire brief — today's posts vs medians."""
import csv, statistics
from collections import defaultdict

PATH = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv'
TODAY = '2026-09-30'

rows = []
with open(PATH, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def to_int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None

# --- 1. Posts dated today ---
tod = [r for r in rows if (r.get('date') or '').strip() == TODAY]
print(f"=== POSTS DATED {TODAY}: {len(tod)} ===")
for r in tod:
    print(f"{r['account']} | views={r['views']} likes={r['likes']} comments={r['comments']} | theme={r['theme']} reel={r['is_reel']} | {r['url']}")

# --- 2. Per-account medians + last post date ---
byacct_v = defaultdict(list)
for r in rows:
    v = to_int(r['views'])
    if v is not None:
        byacct_v[r['account']].append(v)
print("\n=== ACCOUNT MEDIANS ===")
for a, vs in sorted(byacct_v.items()):
    dates = [(r['date'] or '') for r in rows if r['account'] == a]
    print(f"{a}: n={len(vs)} median_views={statistics.median(vs):.0f} max={max(vs)} last_date={max(dates)}")

# --- 3. Theme medians for the two IG lanes ---
for acct in ['drey_ig', 'kevin_ig']:
    bytheme = defaultdict(list)
    for r in rows:
        if r['account'] == acct:
            v = to_int(r['views'])
            if v is not None:
                bytheme[r['theme']].append(v)
    parts = [f"{t}: {statistics.median(v):.0f} (n={len(v)})" for t, v in
             sorted(bytheme.items(), key=lambda kv: -statistics.median(kv[1]))]
    print(f"\n=== {acct} THEME MEDIANS === " + '; '.join(parts))

# --- 4. Last 5 posts per IG account (recency check for evening delta) ---
for acct in ['drey_ig', 'drey_tt', 'kevin_ig', 'kevin_tt']:
    sub = [r for r in rows if r['account'] == acct]
    sub.sort(key=lambda r: (r['ts'] or ''), reverse=True)
    print(f"\n=== LAST 3 {acct} ===")
    for r in sub[:3]:
        print(f"{r['date']} views={r['views']} comments={r['comments']} theme={r['theme']} | {(r['content'] or '')[:70].replace(chr(10),' ')}")
