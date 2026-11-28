# Morning inspire-brief stats 2026-11-28 AM — all quoted numbers come from THIS script only.
# Lookalike rows transcribed from THIS run's tokscript_pull.py stdout (2026-11-28 ~7:00a ET).
import json, csv, statistics, urllib.request, datetime
from zoneinfo import ZoneInfo

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
ET = ZoneInfo('America/New_York')
now = datetime.datetime.now(ET)
print('RUN TIME (ET):', now.isoformat())

def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None

def fmt(x):
    if x is None:
        return 'n/a'
    if x == int(x):
        return f'{int(x):,}'
    return f'{x:,.1f}'

pull = {
    'rowancheung': [('2026-11-27', 20434, 23), ('2026-11-25', 41107, 13), ('2026-11-24', 72137, 21),
                    ('2026-11-23', 90857, 40), ('2026-11-21', 66494, 48), ('2026-11-20', 35215, 5),
                    ('2026-11-19', 17698, 36), ('2026-11-18', 119740, 69), ('2026-11-17', 39804, 13)],
    'bedroskeuilian': [('2026-11-26', 175341, 62), ('2026-11-24', 256518, 41), ('2026-11-22', 234405, 52),
                       ('2026-11-19', 188154, 49), ('2026-11-16', 227543, 41), ('2026-11-12', 407531, 89),
                       ('2026-11-11', 183712, 30), ('2026-11-09', 214721, 62), ('2026-11-06', 77358, 75),
                       ('2026-11-04', 167531, 65), ('2026-11-03', 157035, 49), ('2026-11-02', 364132, 67)],
    'gerardadams': [('2026-11-27', 2953, 5), ('2026-11-24', 135470, 92), ('2026-11-23', 128554, 82),
                    ('2026-11-21', 2081, 3), ('2026-11-20', 128322, 82), ('2026-11-20', 105413, 83),
                    ('2026-11-19', 111187, 81), ('2026-11-18', 123696, 87), ('2026-11-18', 130080, 94),
                    ('2026-11-17', 98685, 79), ('2026-11-16', 136667, 122), ('2026-11-14', 8861, 11)],
    'davidmeltzer': [('2026-11-26', 3629, 3), ('2026-11-26', 3069, 29), ('2026-11-26', 4002, 5),
                     ('2026-11-25', 1966, 7), ('2026-11-25', 1594, 6), ('2026-11-24', 2723, 7),
                     ('2026-11-24', 3264, 8), ('2026-11-23', 4360, 4), ('2026-11-21', 5827, 33),
                     ('2026-11-21', 2527, 8)],
}

print('\n== LOOKALIKES (this run) ==')
rw = [v for _, v, _ in pull['rowancheung']]
print('rowan last-9 median:', fmt(med(rw)), 'n=9 | newest(11-27) 20,434 (was 13,295 yesterday AM)')
bw = [v for _, v, _ in pull['bedroskeuilian']]
streak = 0
for d, v, c in pull['bedroskeuilian']:
    if v >= 170000:
        streak += 1
    else:
        break
print('bedros 12-reel median:', fmt(med(bw)), f'n=12 | >=170k streak from latest: {streak} | newest 11-26 10:31a ET: 175,341/62c')
gc = [v for _, v, _ in pull['gerardadams']]
floors = [v for v in gc if v < 3000]
print('gerard 12-reel median:', fmt(med(gc)), f'n=12 | floors <3k: {len(floors)} ->', floors, '| newest 11-27 12:15p ET: 2,953/5c')
mw = [v for _, v, _ in pull['davidmeltzer']]
print('meltzer last-10 median:', fmt(med(mw)), 'n=10 | 3 reels on 11-26')
print('liam: last post 2026-11-19 ->', (now.date() - datetime.date(2026, 11, 19)).days, 'days silent')

# ---------- founders: CSV ----------
rows = list(csv.DictReader(open(f'{BASE}/posts_all.csv')))

def feed(r):
    return r['content'].strip() != '' and '/stories/' not in r['url']

def num(r, k):
    try:
        return float(r[k])
    except (ValueError, TypeError):
        return None

def ets(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S+00:00').replace(tzinfo=datetime.timezone.utc).astimezone(ET)

drey = [r for r in rows if r['account'] == 'drey_ig' and feed(r)]
kevin = [r for r in rows if r['account'] == 'kevin_ig' and feed(r)]
print(f'\n== FOUNDERS (CSV 6:31a refresh) == drey feed n={len(drey)}, kevin feed n={len(kevin)}')

dreel = [r for r in drey if r['is_reel'] == 'True']
dstat = [r for r in drey if r['is_reel'] == 'False']
ai = [r for r in drey if r['theme'] == 'ai_systems']
cr = [r for r in drey if r['theme'] in ('confession', 'room')]
print('DREY reels median:', fmt(med([num(r, 'views') for r in dreel])), f'n={len(dreel)}',
      '| statics median:', fmt(med([num(r, 'views') for r in dstat])), f'n={len(dstat)}')
print('DREY ai_systems median:', fmt(med([num(r, "views") for r in ai])), f'n={len(ai)}',
      '| confession+room median:', fmt(med([num(r, "views") for r in cr])), f'n={len(cr)}')
best = max(drey, key=lambda r: num(r, 'views') or 0)
print('DREY all-time top feed (CSV):', fmt(num(best, 'views')), best['theme'], best['url'])

eve = [num(r, 'views') for r in dreel if r['date'] >= '2026-11-01' and ets(r['ts']).hour == 0]
noon = [num(r, 'views') for r in dreel if r['date'] >= '2026-11-01' and ets(r['ts']).hour == 17]
print('DREY evening auto slot (00:0x UTC) median:', fmt(med(eve)), f'n={len(eve)}',
      '| noon auto slot (17:0x UTC) median:', fmt(med(noon)), f'n={len(noon)}')

last20 = sorted(drey, key=lambda r: r['ts'])[-20:]
slog = sum(1 for r in last20 if 'Follow for' in r['content'])
coms = sum(num(r, 'comments') or 0 for r in last20)
print(f'DREY last-20 feed: slogan on {slog}/20, total comments {int(coms)}')

kstat = [r for r in kevin if r['is_reel'] == 'False']
kstat_49 = [num(r, 'views') for r in kstat if 16 <= ets(r['ts']).hour <= 21]
kstat_ot = [num(r, 'views') for r in kstat if not (16 <= ets(r['ts']).hour <= 21)]
print('KEVIN statics median:', fmt(med([num(r, "views") for r in kstat])), f'n={len(kstat)}',
      '| statics 4-9p ET median:', fmt(med(kstat_49)), f'n={len(kstat_49)}',
      '| other-times median:', fmt(med(kstat_ot)), f'n={len(kstat_ot)}')
kreel = [r for r in kevin if r['is_reel'] == 'True']
kr_37 = [num(r, 'views') for r in kreel if 15 <= ets(r['ts']).hour <= 19]
kr_ot = [num(r, 'views') for r in kreel if not (15 <= ets(r['ts']).hour <= 19)]
print('KEVIN reels 3-7p ET median:', fmt(med(kr_37)), f'n={len(kr_37)}',
      '| elsewhere median:', fmt(med(kr_ot)), f'n={len(kr_ot)}')
for theme in ('identity', 'room', 'discipline', 'confession'):
    tv = [num(r, 'views') for r in kevin if r['theme'] == theme]
    if tv:
        print(f'KEVIN {theme} median:', fmt(med(tv)), f'n={len(tv)}')

# ---------- fresh Zernio pull ----------
KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
API = 'https://getlate.dev/api/v1'
ACCOUNTS = [('drey_ig', 'instagram', '6a1c7e1e2b2567671a7f25ee'), ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845')]
fresh = {}
for key, platform, aid in ACCOUNTS:
    req = urllib.request.Request(f'{API}/analytics?platform={platform}&accountId={aid}&fromDate=2026-11-22&toDate=2026-11-28&limit=50&page=1',
                                  headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.loads(r.read().decode())
    out = []
    for p in d.get('posts', []):
        an = p.get('analytics') or {}
        out.append({'url': p.get('platformPostUrl'), 'at': p.get('publishedAt'),
                    'views': an.get('views'), 'comments': an.get('comments'), 'likes': an.get('likes')})
    fresh[key] = out
json.dump({'fetched_at': now.isoformat(), 'fresh': fresh}, open(f'{BASE}/raw/am_delta_2026-11-28.json', 'w'), default=str)

print('\n== FRESH ZERNIO (since 11-22) ==')
for k, lst in fresh.items():
    print(f'--- {k} ({len(lst)} posts)')
    for o in sorted(lst, key=lambda x: str(x['at'])):
        dt = datetime.datetime.fromisoformat(str(o['at']).replace('Z', '+00:00')).astimezone(ET)
        age = (now - dt).total_seconds() / 3600
        print(f"  {o['at']} -> {dt.strftime('%m-%d %I:%M%p')} ET | age {age:.1f}h | views={o['views']} com={o['comments']} | {str(o['url'])[-30:]}")

overlay = {str(o['url']): o['views'] for lst in fresh.values() for o in lst}
def val(r):
    v = overlay.get(r['url'])
    return v if v is not None else (num(r, 'views') or 0)
for label, ars in (('DREY', drey), ('KEVIN', kevin)):
    best = max(ars, key=val)
    print(f'{label} top feed (fresh overlay):', fmt(val(best)), best['theme'], best['url'])
krtop = max(kreel, key=val)
print('KEVIN top REEL (fresh overlay):', fmt(val(krtop)), krtop['theme'], krtop['url'], '| posted', ets(krtop['ts']).strftime('%m-%d %I:%M%p ET'))
