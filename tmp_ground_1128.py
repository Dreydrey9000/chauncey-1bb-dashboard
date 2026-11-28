# Ground-truth harness 2026-11-28 AM — recomputes every quoted stat INDEPENDENTLY from
# posts_all.csv + raw/am_delta_2026-11-28.json + this run's transcribed lookalike numbers.
import csv, json, statistics, datetime, re
from zoneinfo import ZoneInfo

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
ET = ZoneInfo('America/New_York')
now = datetime.datetime.now(ET)
src = open(f'{BASE}/site/inspire.js', encoding='utf8').read()

def ets(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S+00:00').replace(tzinfo=datetime.timezone.utc).astimezone(ET)

def med(xs):
    xs = [x for x in xs if x is not None]
    return statistics.median(xs) if xs else None

rows = list(csv.DictReader(open(f'{BASE}/posts_all.csv')))
fresh = json.load(open(f'{BASE}/raw/am_delta_2026-11-28.json'))['fresh']
fmap = {str(o['url']): o for lst in fresh.values() for o in lst}

def feed(r):
    return r['content'].strip() != '' and '/stories/' not in r['url']

def v(r):
    o = fmap.get(r['url'])
    if o is not None and o.get('views') is not None:
        return float(o['views'])
    try:
        return float(r['views'])
    except (ValueError, TypeError):
        return None

drey = [r for r in rows if r['account'] == 'drey_ig' and feed(r)]
kevin = [r for r in rows if r['account'] == 'kevin_ig' and feed(r)]
dreel = [r for r in drey if r['is_reel'] == 'True']
dstat = [r for r in drey if r['is_reel'] == 'False']
ai = [r for r in drey if r['theme'] == 'ai_systems']
cr = [r for r in drey if r['theme'] in ('confession', 'room')]
kstat = [r for r in kevin if r['is_reel'] == 'False']
kreel = [r for r in kevin if r['is_reel'] == 'True']
last20 = sorted(drey, key=lambda r: r['ts'])[-20:]

checks, fails = [], []
def chk(name, got, want, exact=True, tol=0.01):
    ok = (got == want) if exact else abs(got - want) / max(1e-9, abs(want)) <= tol
    (checks if ok else fails).append(f"{'ok  ' if ok else 'FAIL'} {name}: got {got!r} want {want!r}")

# DREY quotes
chk('confession+room median (n=8)', (med([v(r) for r in cr]), len(cr)), (1432.0, 8))
chk('ai_systems median (n=45)', (med([v(r) for r in ai]), len(ai)), (203.0, 45))
chk('drey top feed', max(x for x in (v(r) for r in drey) if x is not None), 3871.0)
chk('slogan last 20', sum(1 for r in last20 if 'Follow for' in r['content']), 19)
chk('comments last 20', sum(float(r['comments'] or 0) for r in last20), 0.0)
chk('drey statics median (n=8)', (med([v(r) for r in dstat]), len(dstat)), (423.0, 8))
chk('drey reels median (n=52)', (med([v(r) for r in dreel]), len(dreel)), (174.5, 52))
noon = [v(r) for r in dreel if r['date'] >= '2026-11-01' and ets(r['ts']).hour == 12]
eve = [v(r) for r in dreel if r['date'] >= '2026-11-01' and ets(r['ts']).hour == 19]
chk('noon slot median ~140', med(noon), 140.0, exact=False)
chk('eve slot median ~140', med(eve), 139.0, exact=False)
mid = fmap.get('https://www.instagram.com/reel/DgOWCZZIXQG/')
noonr = fmap.get('https://www.instagram.com/reel/DgQK_4Nox2Q/')
chk('midnight reel fresh views', float(mid['views']), 203.0)
chk('noon reel fresh views', float(noonr['views']), 140.0)
chk('compute reel 995', v([r for r in dreel if 'DgLBOOBh3nn' in r['url']][0]), 995.0)
chk('7.0x cr/ai', 1432.0 / 203.0, 7.0, exact=False)
chk('4.9x compute', 995.0 / 203.0, 4.9, exact=False)
chk('2.4x statics/reels', round(423.0 / 174.5, 1), 2.4)
chk('$200 and $20,000 in Drey own caption', ('200' in [r for r in drey if 'DgLBOOBh3nn' in r['url']][0]['content'], '20,000' in [r for r in drey if 'DgLBOOBh3nn' in r['url']][0]['content']), (True, True))

# KEVIN quotes
chk('kevin statics median (n=70)', (med([v(r) for r in kstat]), len(kstat)), (2004.0, 70))
k49 = [v(r) for r in kstat if 16 <= ets(r['ts']).hour <= 21]
kot = [v(r) for r in kstat if not (16 <= ets(r['ts']).hour <= 21)]
chk('statics 4-9p (n=22)', (med(k49), len(k49)), (2626.0, 22))
chk('statics other', med(kot), 1738.0)
k37 = [v(r) for r in kreel if 15 <= ets(r['ts']).hour <= 19]
krot = [v(r) for r in kreel if not (15 <= ets(r['ts']).hour <= 19)]
chk('reels 3-7p (n=18)', (med(k37), len(k37)), (1295.0, 18))
chk('reels elsewhere', med(krot), 852.0)
chk('identity median (n=18)', (med([v(r) for r in kevin if r['theme'] == 'identity']), len([r for r in kevin if r['theme'] == 'identity'])), (2207.5, 18))
chk('room median (n=35)', (med([v(r) for r in kevin if r['theme'] == 'room']), len([r for r in kevin if r['theme'] == 'room'])), (1763.0, 35))
top_reel = max(kreel, key=lambda r: (v(r) or 0))
chk('kevin top reel', (v(top_reel), 'DgIUQyCjMAT' in top_reel['url']), (7231.0, True))
chk('4.1x room', 7231.0 / 1763.0, 4.1, exact=False)
for u, want in (('DgIrvbfgPex', 1643.0), ('DgLOx8wEeIk', 867.0), ('DgP2IHuiHn7', 689.0)):
    chk('static ' + u, v([r for r in kstat if u in r['url']][0]), want)
chk('82% of median', 1643.0 / 2004.0, 0.82, exact=False)
chk('43% of median', 867.0 / 2004.0, 0.43, exact=False)
chk('34% of median', round(689.0 / 2004.0, 2), 0.34)
w = [r for r in kevin if 'weight was all on my shoulders' in r['content']]
chk('kevin 11-25 weight quote', (len(w) == 1, w[0]['date'] if w else None), (True, '2026-11-25'))
rr = [r for r in kreel if 'DgIUQyCjMAT' in r['url']][0]
chk('room reel caption has sequel question', 'What rooms are you in' in rr['content'], True)

# LOOKALIKE quotes (transcribed from this run's tokscript stdout)
rowan = [(27, 20434, 23), (25, 41107, 13), (24, 72137, 21), (23, 90857, 40), (21, 66494, 48),
         (20, 35215, 5), (19, 17698, 36), (18, 119740, 69), (17, 39804, 13)]
chk('rowan last-9 median', med([x[1] for x in rowan]), 41107.0)
chk('rowan comment median', med([x[2] for x in rowan]), 23)
chk('rowan 9 reels in 10 days', (len(rowan), 27 - 17), (9, 10))
chk('rowan +54% overnight', 20434.0 / 13295.0, 1.54, exact=False)
bedros = [175341, 256518, 234405, 188154, 227543, 407531, 183712, 214721, 77358, 167531, 157035, 364132]
chk('bedros 12-median', med(bedros), 201437.5)
streak = 0
for x in bedros:
    if x >= 170000:
        streak += 1
    else:
        break
chk('bedros 8th straight >=170k', streak, 8)
gerard_floors = [2953, 2081]
chk('gerard floors 2 of 12', len(gerard_floors), 2)
g = fmap and None
age = (now - datetime.datetime(2026, 11, 27, 12, 15, 27, tzinfo=ET)).total_seconds() / 3600
chk('gerard newest ~19h old (12:15p ET post)', 18 < age < 20.5, True)
melt = [3629, 3069, 4002, 1966, 1594, 2723, 3264, 4360, 5827, 2527]
chk('meltzer last-10 median', med(melt), 3166.5)
chk('liam 9 days silent', (now.date() - datetime.date(2026, 11, 19)).days, 9)

print('\n'.join(checks))
if fails:
    print('\n' + '\n'.join(fails))
    raise SystemExit('GROUND TRUTH FAIL: ' + str(len(fails)) + ' checks failed')
print('GROUND TRUTH PASS: ' + str(len(checks)) + ' checks')
