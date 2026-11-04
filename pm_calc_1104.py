#!/usr/bin/env python3
"""PM 1104: medians from posts_all.csv + beat/miss for today's posts (pm_delta json)."""
import csv, json, os, statistics, datetime
BASE = os.path.dirname(os.path.abspath(__file__))

rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
print('CSV max date per account:')
for acc in ('drey_ig', 'kevin_ig'):
    ds = [r['date'] for r in rows if r['account'] == acc and r['date']]
    print(f'  {acc}: max={max(ds)} n={len(ds)}')

TODAY = '2026-11-04'
def med(vals):
    return statistics.median(vals) if vals else None

# Drey: 14d theme medians
cut = (datetime.date.today() - datetime.timedelta(days=14)).isoformat()
d14 = [r for r in rows if r['account'] == 'drey_ig' and r['date'] >= cut]
themes = {}
for r in d14:
    try:
        v = int(float(r['views'] or 0))
    except Exception:
        continue
    themes.setdefault(r['theme'], []).append(v)
print(f'\nDREY 14d (since {cut}) theme medians:')
for t, vs in sorted(themes.items(), key=lambda kv: -med(kv[1])):
    print(f'  {t}: median={med(vs)} n={len(vs)}')

# Kevin: 7d reel vs static
cut7 = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()
k7 = [r for r in rows if r['account'] == 'kevin_ig' and r['date'] >= cut7]
st = [int(float(r['views'] or 0)) for r in k7 if r['is_reel'] == 'False']
rl = [int(float(r['views'] or 0)) for r in k7 if r['is_reel'] == 'True']
print(f'\nKEVIN 7d (since {cut7}): statics median={med(st)} n={len(st)} | reels median={med(rl)} n={len(rl)}')

# Today's posts beat/miss
print('\nTODAY (2026-11-04 ET) beat/miss:')
dj = json.load(open(os.path.join(BASE, 'raw', f'pm_delta_{TODAY}.json')))['fresh']
ref = {
    ('drey_ig', 'ai_systems'): med(themes.get('ai_systems', [])),
    ('drey_ig', 'room'): med(themes.get('room', themes.get('room_confession', []))),
}
for acc, posts in dj.items():
    if not isinstance(posts, list):
        continue
    for p in posts:
        ts = str(p.get('posted_at') or '')
        if not ts.startswith(TODAY):
            continue
        et = (datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
              - datetime.timedelta(hours=5))
        print(f"  {acc} {et.strftime('%H:%M')}ET reel={'/reel/' in str(p.get('url'))} views={p.get('views')} likes={p.get('likes')} comments={p.get('comments')} :: {str(p.get('caption'))[:60]!r}")
print('\nREF medians for call: drey room/confession 14d =', themes.get('room') or themes.get('room_confession'))
