#!/usr/bin/env python3
"""AM brief stats 2026-11-03 — founder lanes from posts_all.csv (6:31a pull)."""
import csv, statistics as st
from collections import defaultdict

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
for r in rows:
    r['views_n'] = int(r['views'] or 0)

def med(vals):
    vals = sorted(vals)
    return st.median(vals) if vals else None

# 7d window: 2026-10-27 .. 2026-11-03 (inclusive) = trailing week
W = [r for r in rows if '2026-10-27' <= r['date'] <= '2026-11-03']

for who, pref in (('DREY', 'drey'), ('KEVIN', 'kevin')):
    ig = [r for r in W if r['account'] == pref + '_ig']
    reels = [r for r in ig if r['is_reel'] == 'True']
    statics = [r for r in ig if r['is_reel'] == 'False']
    print(f'== {who} IG 7d (10-27..11-03): {len(ig)} posts | reels n={len(reels)} median={med([r["views_n"] for r in reels])} | statics n={len(statics)} median={med([r["views_n"] for r in statics])}')

# Drey 11-03 overnight queue (times are UTC; ET = -5h)
print('\n== DREY posts dated 2026-11-03 (overnight ET):')
for r in rows:
    if r['date'] == '2026-11-03' and r['account'] == 'drey_ig':
        print(f"  {r['ts'][11:16]}Z reel={r['is_reel']} views={r['views_n']:>5} likes={r['likes']:>3} comments={r['comments']} watch_ms={r['watch_ms']} dur={r['dur_s']}s theme={r['theme']}")
        print(f"     {r['url']}")

# Drey theme split, last 14d
W14 = [r for r in rows if '2026-10-20' <= r['date'] <= '2026-11-03' and r['account'] == 'drey_ig' and r['is_reel'] == 'True']
themes = defaultdict(list)
for r in W14:
    themes[r['theme']].append(r['views_n'])
print('\n== DREY reel views by theme (14d):')
for t, v in sorted(themes.items(), key=lambda kv: -st.median(kv[1])):
    print(f'  {t}: n={len(v)} median={st.median(v):.0f} max={max(v)}')

# tool-lane reels individually (Drey), 14d
print('\n== DREY ai_systems reels 14d detail:')
for r in W14:
    if r['theme'] == 'ai_systems':
        print(f"  {r['date']} {r['views_n']:>5} views  {r['url']}")

# Kevin: identity vs room reels, 14d
W14k = [r for r in rows if '2026-10-20' <= r['date'] <= '2026-11-03' and r['account'] == 'kevin_ig' and r['is_reel'] == 'True']
tk = defaultdict(list)
for r in W14k:
    tk[r['theme']].append(r['views_n'])
print('\n== KEVIN reel views by theme (14d):')
for t, v in sorted(tk.items(), key=lambda kv: -st.median(kv[1])):
    print(f'  {t}: n={len(v)} median={st.median(v):.0f} max={max(v)}')

# Kevin 11-01 identity reel maturity + 11-02 finals
print('\n== KEVIN recent checkpoints:')
for r in rows:
    if r['account'] == 'kevin_ig' and r['date'] in ('2026-11-01', '2026-11-02'):
        print(f"  {r['date']} {r['ts'][11:16]}Z reel={r['is_reel']} views={r['views_n']:>5} theme={r['theme']} | {r['url']}")

# last post before the overnight queue (dark-day check)
drey_prev = [r for r in rows if r['account'] == 'drey_ig' and r['date'] < '2026-11-03']
print(f"\nDrey previous IG post before 11-03 queue: {drey_prev[-1]['date']} {drey_prev[-1]['ts'][11:16]}Z views={drey_prev[-1]['views_n']} theme={drey_prev[-1]['theme']}")
kev_today = [r for r in rows if r['date'] == '2026-11-03' and r['account'].startswith('kevin')]
print(f'Kevin posts on 11-03 so far: {len(kev_today)}')
