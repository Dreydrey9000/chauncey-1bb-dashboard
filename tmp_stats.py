#!/usr/bin/env python3
"""Morning brief stats: medians by founder/theme/format from posts_all.csv."""
import csv, statistics as st
from collections import defaultdict

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
for r in rows:
    r['views'] = int(r['views'] or 0)
    r['comments'] = int(r['comments'] or 0)
    r['is_reel'] = r['is_reel'] == 'True'

def med(vals):
    vals = [v for v in vals if v > 0]
    return (round(st.median(vals)), len(vals)) if vals else (None, 0)

for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    print(f'== {acct} n={len(sub)} ==')
    bytheme = defaultdict(list)
    for r in sub:
        bytheme[r['theme']].append(r['views'])
    for t, v in sorted(bytheme.items(), key=lambda kv: -st.median([x for x in kv[1] if x > 0] or [0])):
        m, n = med(v)
        if m: print(f'  theme {t:12s} median={m:5d} n={n}')
    reels = [r['views'] for r in sub if r['is_reel'] and r['views'] > 0]
    statics = [r['views'] for r in sub if not r['is_reel'] and r['views'] > 0]
    print(f'  REELS median={st.median(reels):.0f} n={len(reels)} | STATICS median={st.median(statics):.0f} n={len(statics)}')
    print('  -- last 8 posts (newest first):')
    for r in sorted(sub, key=lambda x: x['ts'], reverse=True)[:8]:
        print(f"    {r['date']} {'REEL' if r['is_reel'] else 'STAT'} {r['theme']:12s} v={r['views']:5d} c={r['comments']:3d} er={r['er']:>5s}")

# grading: Drey ai_systems reel streak
d = sorted([r for r in rows if r['account'] == 'drey_ig'], key=lambda x: x['ts'], reverse=True)
streak = 0
for r in d:
    if r['theme'] == 'ai_systems':
        streak += 1
    else:
        break
print(f'\nDrey ai_systems streak: {streak} consecutive posts, views: {[r["views"] for r in d[:streak]]}')
# Kevin comment rate on recent reels
k = sorted([r for r in rows if r['account'] == 'kevin_ig' and r['is_reel']], key=lambda x: x['ts'], reverse=True)[:6]
print('Kevin recent reels v/c:', [(r['date'], r['views'], r['comments'], r['theme']) for r in k])
# Kevin static grading (Nov 7 8:11pm ET post)
tgt = [r for r in rows if r['url'] == 'https://www.instagram.com/p/DfdgaVPSuLP/']
print('Kevin identity static DfdgaVPSuLP now:', [(r['views'], r['comments'], r['likes']) for r in tgt])
