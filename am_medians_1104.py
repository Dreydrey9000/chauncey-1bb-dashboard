#!/usr/bin/env python3
"""AM inspire medians — 2026-11-04. From posts_all.csv (refreshed by 6:30a cron)."""
import csv, statistics, datetime, collections, os

BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        try:
            r['v'] = int(float(r['views'] or 0))
        except Exception:
            r['v'] = None
        rows.append(r)

today = datetime.date(2026, 11, 4)

def show(label, rs):
    vs = [r['v'] for r in rs if r['v'] is not None]
    if vs:
        print(f'{label}: n={len(vs)} median={statistics.median(vs):.1f} max={max(vs)}')
    else:
        print(f'{label}: n=0')

# freshness check
fresh = [r for r in rows if r['date'] >= '2026-11-03']
print('--- posts dated Nov 3+ in CSV:', len(fresh))
for r in sorted(fresh, key=lambda x: x['ts']):
    print(f"  {r['account']} {r['ts'][:16]} reel={r['is_reel']} {r['theme']:12s} v={r['v']} c={r['comments']} | {r['url']}")

# Drey last 14d
d14 = [r for r in rows if r['account'] == 'drey_ig' and r['date'] >= '2026-10-21']
show('DREY 14d all', d14)
by = collections.defaultdict(list)
for r in d14:
    by[(r['theme'], r['is_reel'])].append(r)
for k in sorted(by):
    show(f'DREY 14d theme={k[0]} reel={k[1]}', by[k])
# ai_systems lane regardless of reel
show('DREY 14d ai_systems (all formats)', [r for r in d14 if r['theme'] == 'ai_systems'])
show('DREY 14d room/confession', [r for r in d14 if r['theme'] in ('room', 'confession')])
# post-10pm vs evening slot for drey 14d
late = [r for r in d14 if r['ts'][11:13] >= '03' and r['ts'][11:13] <= '08']
print('--- DREY 14d posts 10pm-3am ET (ts 03-08 UTC):', len(late), 'median', statistics.median([r['v'] for r in late if r['v'] is not None]))

# Kevin last 7d
k7 = [r for r in rows if r['account'] == 'kevin_ig' and r['date'] >= '2026-10-28']
show('KEVIN 7d all', k7)
show('KEVIN 7d statics', [r for r in k7 if r['is_reel'] == 'False'])
show('KEVIN 7d reels', [r for r in k7 if r['is_reel'] == 'True'])
byk = collections.defaultdict(list)
for r in k7:
    byk[(r['theme'], r['is_reel'])].append(r)
for k in sorted(byk):
    show(f'KEVIN 7d theme={k[0]} reel={k[1]}', byk[k])
print('--- KEVIN 7d detail:')
for r in sorted(k7, key=lambda x: x['ts']):
    print(f"  {r['ts'][:16]} reel={r['is_reel']} {r['theme']:12s} v={r['v']} l={r['likes']} c={r['comments']} | {str(r['content'])[:60]!r}")
