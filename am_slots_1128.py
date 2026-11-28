# Corrected slot medians for Drey's auto slots (2026-11-28 AM) — quotes from THIS script only.
import csv, statistics, datetime
from zoneinfo import ZoneInfo

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
ET = ZoneInfo('America/New_York')

def ets(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S+00:00').replace(tzinfo=datetime.timezone.utc).astimezone(ET)

def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None

def fmt(x):
    if x is None:
        return 'n/a'
    return f'{int(x):,}' if x == int(x) else f'{x:,.1f}'

rows = list(csv.DictReader(open(f'{BASE}/posts_all.csv')))

def feed(r):
    return r['content'].strip() != '' and '/stories/' not in r['url']

def num(r, k):
    try:
        return float(r[k])
    except (ValueError, TypeError):
        return None

drey_reels = [r for r in rows if r['account'] == 'drey_ig' and feed(r) and r['is_reel'] == 'True']
noon = [num(r, 'views') for r in drey_reels if r['date'] >= '2026-11-01' and ets(r['ts']).hour == 12]
eve = [num(r, 'views') for r in drey_reels if r['date'] >= '2026-11-01' and ets(r['ts']).hour == 19]
print('DREY NOON slot (12pm ET) since 11-01: median', fmt(med(noon)), f'n={len(noon)}', noon)
print('DREY EVENING slot (7pm ET) since 11-01: median', fmt(med(eve)), f'n={len(eve)}', eve)

# Rowan comment median, last 9 reels (this run's pull)
rowan_c = [23, 13, 21, 40, 48, 5, 36, 69, 13]
print('ROWAN last-9 comment median:', fmt(med(rowan_c)))

# Drey last-20 slogan/comments recheck with fresh 11-27 posts
drey_feed = [r for r in rows if r['account'] == 'drey_ig' and feed(r)]
last20 = sorted(drey_feed, key=lambda r: r['ts'])[-20:]
slog = sum(1 for r in last20 if 'Follow for' in r['content'])
coms = sum(num(r, 'comments') or 0 for r in last20)
print(f'DREY last-20 feed: slogan on {slog}/20, total comments {int(coms)}')

# Kevin: completed statics since 11-24 (grade material)
kstat = [r for r in rows if r['account'] == 'kevin_ig' and feed(r) and r['is_reel'] == 'False' and r['date'] >= '2026-11-24']
for r in sorted(kstat, key=lambda r: r['ts']):
    print(f"KEVIN static {r['date']} {ets(r['ts']).strftime('%I:%M%p')} ET views={int(num(r, 'views') or 0):,} com={r['comments']} theme={r['theme']}")

# Kevin reels 3-7p ET recheck (quoted today)
kevin_reels = [r for r in rows if r['account'] == 'kevin_ig' and feed(r) and r['is_reel'] == 'True']
kr_37 = [num(r, 'views') for r in kevin_reels if 15 <= ets(r['ts']).hour <= 19]
kr_ot = [num(r, 'views') for r in kevin_reels if not (15 <= ets(r['ts']).hour <= 19)]
print('KEVIN reels 3-7p ET median:', fmt(med(kr_37)), f'n={len(kr_37)}', '| elsewhere:', fmt(med(kr_ot)), f'n={len(kr_ot)}')
kstat49 = [num(r, 'views') for r in rows if r['account'] == 'kevin_ig' and feed(r) and r['is_reel'] == 'False' and 16 <= ets(r['ts']).hour <= 21]
kstatot = [num(r, 'views') for r in rows if r['account'] == 'kevin_ig' and feed(r) and r['is_reel'] == 'False' and not (16 <= ets(r['ts']).hour <= 21)]
print('KEVIN statics 4-9p ET median:', fmt(med(kstat49)), f'n={len(kstat49)}', '| other:', fmt(med(kstatot)), f'n={len(kstatot)}')
