# PM delta analysis for evening inspire brief — reads posts_all.csv, prints today's/yesterday's posts vs medians
import csv, os, statistics as st
from collections import defaultdict
from datetime import datetime, timezone

P = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(os.path.join(P, 'posts_all.csv'), encoding='utf-8')))
print('total rows:', len(rows))

def iv(s):
    try:
        return int(float(s or 0))
    except ValueError:
        return None

TODAY = '2026-09-29'
print('=== posts dated', TODAY, '===')
n = 0
for r in rows:
    if r['date'] == TODAY:
        n += 1
        print(f"{r['account']} {r['url']} views={r['views']} likes={r['likes']} comments={r['comments']} shares={r['shares']} saves={r['saves']} theme={r['theme']} reel={r['is_reel']}")
        print('   ', r['content'][:120].replace('\n', ' '))
if n == 0:
    print('(none — no posts dated today in synced CSV)')

print('=== posts dated 2026-09-28 (ET evening boundary) ===')
for r in rows:
    if r['date'] == '2026-09-28':
        print(f"{r['account']} ts={r['ts'][:16]} {r['url']} views={r['views']} likes={r['likes']} comments={r['comments']} shares={r['shares']} saves={r['saves']} theme={r['theme']} reel={r['is_reel']}")

print('=== medians by account ===')
med = defaultdict(list)
for r in rows:
    v = iv(r['views'])
    if v is not None:
        med[r['account']].append(v)
for k, v in sorted(med.items()):
    print(f'{k}: n={len(v)} median_views={st.median(v):.0f}')

print('=== drey_ig reels only: median + last 4 reels ===')
dreel = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and iv(r['views']) is not None]
dv = [iv(r['views']) for r in dreel]
print('drey_ig reels n=%d median=%.0f' % (len(dv), st.median(dv)))
for r in dreel[-4:]:
    print(f"  {r['date']} views={r['views']} theme={r['theme']} {r['url']}")

print('=== drey_ig reel medians by theme ===')
tmed = defaultdict(list)
for r in dreel:
    tmed[r['theme']].append(iv(r['views']))
for k, v in sorted(tmed.items(), key=lambda x: -st.median(x[1])):
    print(f'  {k}: n={len(v)} median={st.median(v):.0f}')

print('=== kevin_ig: reels vs statics + theme medians ===')
kig = [r for r in rows if r['account'] == 'kevin_ig' and iv(r['views']) is not None]
kr = [iv(r['views']) for r in kig if r['is_reel'] == 'True']
ks = [iv(r['views']) for r in kig if r['is_reel'] == 'False']
print(f'kevin_ig reels n={len(kr)} median={st.median(kr):.0f} | statics n={len(ks)} median={st.median(ks):.0f}')
kt = defaultdict(list)
for r in kig:
    kt[r['theme']].append(iv(r['views']))
for k, v in sorted(kt.items(), key=lambda x: -st.median(x[1])):
    print(f'  {k}: n={len(v)} median={st.median(v):.0f}')

print('=== last post per founder account ===')
for acc in ('drey_ig', 'drey_tt', 'kevin_ig', 'kevin_tt'):
    mine = [r for r in rows if r['account'] == acc]
    if mine:
        r = mine[-1]
        print(f"{acc}: last {r['date']} views={r['views']} theme={r['theme']} reel={r['is_reel']}")

print('=== sync freshness ===')
for f in ('posts_all.csv', 'site/data.js', 'gen_data.py'):
    fp = os.path.join(P, f)
    if os.path.exists(fp):
        print(f, datetime.fromtimestamp(os.path.getmtime(fp), tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))
rawd = os.path.join(P, 'raw')
if os.path.isdir(rawd):
    fs = sorted((os.path.getmtime(os.path.join(rawd, f)), f) for f in os.listdir(rawd))
    for mt, f in fs[-4:]:
        print('raw/', f, datetime.fromtimestamp(mt, tz=timezone.utc).strftime('%Y-%m-%d %H:%M UTC'))
