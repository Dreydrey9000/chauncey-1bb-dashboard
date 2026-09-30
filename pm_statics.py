#!/usr/bin/env python3
"""Verify Kevin IG statics vs reels, last 7 days (2026-09-24..09-30), from posts_all.csv."""
import csv

rows = [r for r in csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv', newline='', encoding='utf-8'))]

def to_int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None

for acct in ['kevin_ig', 'kevin_tt']:
    print(f"===== {acct}, 2026-09-24 onward =====")
    sub = [r for r in rows if r['account'] == acct and (r.get('date') or '') >= '2026-09-24']
    sub.sort(key=lambda r: r['ts'] or '')
    for r in sub:
        reel = r['is_reel'].strip().lower() == 'true'
        print(f"{r['date']} {'REEL ' if reel else 'STATIC'} views={r['views']:>5} comments={r['comments']:>2} theme={r['theme']:<10} | {(r['content'] or '')[:55].replace(chr(10), ' ')}")
    reels = [v for r in sub if r['is_reel'].strip().lower() == 'true' for v in [to_int(r['views'])] if v is not None]
    stats = [v for r in sub if r['is_reel'].strip().lower() != 'true' for v in [to_int(r['views'])] if v is not None]
    if reels: print(f"  reels avg {sum(reels)/len(reels):.0f} (n={len(reels)})")
    if stats: print(f"  statics avg {sum(stats)/len(stats):.0f} (n={len(stats)})")

# Drey Aug 30 confession reel verification
print("\n===== drey_ig 2026-08-28..09-01 =====")
for r in rows:
    if r['account'] == 'drey_ig' and '2026-08-28' <= (r.get('date') or '') <= '2026-09-01':
        print(f"{r['date']} {'REEL' if r['is_reel'].strip().lower()=='true' else 'STATIC'} views={r['views']} comments={r['comments']} theme={r['theme']} | {(r['content'] or '')[:55].replace(chr(10),' ')}")
