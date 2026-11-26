# Inspire-brief PM helper 6 — 2026-11-26 evening. Window medians quoted in tonight's brief.
# Kevin reels 3-7p vs other; Drey reels noon vs 7p slot (mature posts only, >=48h at 6:31a snapshot).
import csv, statistics, datetime
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))

def hour_et(p):
    t = str(p.get('ts', ''))
    try:
        dt = datetime.datetime.strptime(t[:19], '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None, None
    e = dt - datetime.timedelta(hours=5)
    return e.hour, e

def views(p):
    try:
        return int(float(p['views'] or 0))
    except Exception:
        return None

def feed(acc):
    return [r for r in rows if r['account'] == acc and '/stories/' not in str(r.get('url', ''))]

print('=== Kevin FEED REELS by ET window ===')
w = {'15-19 (3-7p)': [], 'other': []}
for p in feed('kevin_ig'):
    if p['is_reel'] == 'True' and '/reel/' in str(p.get('url', '')):
        h, _ = hour_et(p)
        v = views(p)
        if h is None or v is None:
            continue
        w['15-19 (3-7p)' if 15 <= h < 19 else 'other'].append(v)
for k, vs in w.items():
    print(f'{k}: n={len(vs)} median={repr(statistics.median(vs))}')

print()
print('=== Drey FEED REELS by slot (mature only: ts <= 2026-11-24T12:00Z, i.e. >=48h at 6:31a snapshot) ===')
CUT = datetime.datetime(2026, 11, 24, 12, 0)
s = {'noon (11a-1p)': [], '7p (6-8p)': [], 'other': []}
for p in feed('drey_ig'):
    if p['is_reel'] == 'True' and '/reel/' in str(p.get('url', '')):
        h, e = hour_et(p)
        v = views(p)
        if h is None or v is None or e is None or e > CUT:
            continue
        if 11 <= h < 13:
            s['noon (11a-1p)'].append(v)
        elif 18 <= h < 20:
            s['7p (6-8p)'].append(v)
        else:
            s['other'].append(v)
for k, vs in s.items():
    if vs:
        print(f'{k}: n={len(vs)} median={repr(statistics.median(vs))}')

print()
print('=== Kevin identity static trajectory ===')
print('DgLOx8wEeIk: 610 (6:31a CSV) -> 669 (6p fresh) = +' + str(669-610))
print('=== Drey yesterday-noon reel trajectory ===')
print('DgLBOOBh3nn: 702 (6:31a CSV) -> 995 (6p fresh) = +' + str(995-702))
