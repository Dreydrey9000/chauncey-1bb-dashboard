# Inspire-brief PM helper 7 — 2026-11-26 evening. Kevin feed STATICS by ET window (recompute; stats4 block was empty).
import csv, statistics, datetime
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))

def hour_et(p):
    t = str(p.get('ts', ''))
    try:
        dt = datetime.datetime.strptime(t[:19], '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None
    return (dt - datetime.timedelta(hours=5)).hour

def views(p):
    try:
        return int(float(p['views'] or 0))
    except Exception:
        return None

w = {'13-16 (1-4p)': [], '16-21 (4-9p)': [], 'other': []}
n_total = 0
n_skipped = 0
for p in rows:
    if p['account'] != 'kevin_ig':
        continue
    if '/stories/' in str(p.get('url', '')):
        continue
    if p['is_reel'] != 'False' or '/p/' not in str(p.get('url', '')):
        continue
    n_total += 1
    h = hour_et(p)
    v = views(p)
    if h is None or v is None:
        n_skipped += 1
        continue
    if 13 <= h < 16:
        w['13-16 (1-4p)'].append(v)
    elif 16 <= h < 21:
        w['16-21 (4-9p)'].append(v)
    else:
        w['other'].append(v)
print(f'kevin feed statics total={n_total}, skipped(no ts/views)={n_skipped}')
for k, vs in sorted(w.items()):
    if vs:
        print(f'{k}: n={len(vs)} median={repr(statistics.median(vs))}')
