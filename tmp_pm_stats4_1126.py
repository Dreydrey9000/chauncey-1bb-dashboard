# Inspire-brief PM helper 4 (FINAL) — 2026-11-26 evening. Locks every quoted number.
# Basis rules: feed-only (stories excluded), type = is_reel flag AND URL shape.
# Medians printed with repr() — no int() truncation.
import csv, statistics, datetime, json
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))

def feed(acc):
    return [r for r in rows if r['account'] == acc and '/stories/' not in str(r.get('url', ''))]

def views(p):
    try:
        return int(float(p['views'] or 0))
    except Exception:
        return None

print('=== FINAL medians (feed-only, flag+URL cross-checked) ===')
for acc in ('drey_ig', 'kevin_ig'):
    fr = [p for p in feed(acc) if p['is_reel'] == 'True' and '/reel/' in str(p.get('url', ''))]
    fs = [p for p in feed(acc) if p['is_reel'] == 'False' and '/p/' in str(p.get('url', ''))]
    mr = [views(p) for p in fr]; mr = [v for v in mr if v is not None]
    ms = [views(p) for p in fs]; ms = [v for v in ms if v is not None]
    print(f'{acc} FEED REELS: n={len(mr)} median={repr(statistics.median(mr))}')
    print(f'{acc} FEED STATICS: n={len(ms)} median={repr(statistics.median(ms))}')

print()
print('=== Kevin statics by ET hour window (from ts, UTC-5) ===')
def hour_et(p):
    t = str(p.get('ts', ''))
    try:
        dt = datetime.datetime.strptime(t[:19], '%Y-%m-%d %H:%M:%S')
    except Exception:
        return None
    return (dt - datetime.timedelta(hours=5)).hour
w = {'13-16': [], '16-21': [], 'other': []}
for p in feed('kevin_ig'):
    if p['is_reel'] == 'False' and '/p/' in str(p.get('url', '')):
        h = hour_et(p)
        v = views(p)
        if h is None or v is None:
            continue
        if 13 <= h < 16:
            w['13-16'].append(v)
        elif 16 <= h < 21:
            w['16-21'].append(v)
        else:
            w['other'].append(v)
for k, vs in w.items():
    if vs:
        print(f'{k}p ET: n={len(vs)} median={repr(statistics.median(vs))}')

print()
print('=== Drey today vs median (final basis) ===')
med_drey_reels = 179  # from above; will re-derive programmatically below
fr = [p for p in feed('drey_ig') if p['is_reel'] == 'True' and '/reel/' in str(p.get('url', ''))]
med = statistics.median([v for v in (views(p) for p in fr) if v is not None])
print(f'Drey reel median = {repr(med)}')
print(f'7p reel 152 @ ~23h: {round(152/med*100, 1)}% of median')
print(f'Nov25 noon reel 995 @ ~28h: {round(995/med, 1)}x median; 702->995 = +{round((995-702)/702*100, 1)}% since 6:31a CSV')

print()
print('=== Kevin statics median + identity static (final basis) ===')
fs = [p for p in feed('kevin_ig') if p['is_reel'] == 'False' and '/p/' in str(p.get('url', ''))]
meds = statistics.median([v for v in (views(p) for p in fs) if v is not None])
print(f'Kevin feed statics median = {repr(meds)}')
print(f'identity static 669 @ ~28h: {round(669/meds*100, 1)}% of median; needs {2000-669} more views by ~2p tomorrow for the 2,000@48h prediction')

print()
print('=== misc quoted ===')
print(f'Drey statics 469 vs reels 179: {round(469/179, 1)}x')
print(f'rowan 29191->35792: +{round((35792-29191)/29191*100, 1)}%')
print(f'Kevin room reel 6859 vs volleyball 6686: +{6859-6686}')
print('bedros new-today reel age: posted 15:31:48Z, pulled ~23:05Z = ~7.5h')
print('meltzer reels since yesterday 7p ET: 3640, 2100, 2712 (none over 3,640)')
print('liam last post 2026-11-19T19:00Z -> at 2026-11-26T23:00Z = 7 days 4 hours')
