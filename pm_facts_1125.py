#!/usr/bin/env python3
"""PM 2026-11-25 extras: full captions for today's posts + CSV facts (slogan count, last static, evening statics)."""
import csv, json, urllib.request, datetime, statistics

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
API = 'https://getlate.dev/api/v1'

ACCOUNTS = [
    ('drey_ig',  'instagram', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845'),
]

def get(path):
    req = urllib.request.Request(f'{API}/{path}', headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

print('#### FULL CAPTIONS: posts published 2026-11-24T12:00Z onward ####')
for key, platform, aid in ACCOUNTS:
    d = get(f'analytics?platform={platform}&accountId={aid}&fromDate=2026-11-24&toDate=2026-11-25&limit=50&page=1')
    for p in d.get('posts', []):
        ts = p.get('publishedAt') or ''
        if ts < '2026-11-24T12:00':
            continue
        an = p.get('analytics') or {}
        url = p.get('platformPostUrl') or ''
        if '/stories/' in url:
            continue
        print(f"== {key} {ts} views={an.get('views')} likes={an.get('likes')} com={an.get('comments')}")
        print(f"   {url}")
        print('   FULL CAPTION:')
        print('   ' + str(p.get('content') or '').replace('\n', '\n   | '))
        print()

print('#### CSV FACTS ####')
rows = [r for r in csv.DictReader(open(BASE + '/posts_all.csv', newline='', encoding='utf-8'))]

def is_story(r):
    return '/stories/' in r['url'] or not r['content'].strip()

# Drey: last 15 reels with captions (tail)
drey_reels = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and not is_story(r)]
drey_reels.sort(key=lambda r: r['ts'])
print(f"Drey reels total in csv: {len(drey_reels)}; last 15 tails:")
slogan_count = 0
for r in drey_reels[-15:]:
    cap = r['content'].strip()
    tail = cap[-90:].replace('\n', ' / ')
    has_slogan = ('follow for ai' in cap.lower()) or ('follow for a.i' in cap.lower())
    if has_slogan:
        slogan_count += 1
    print(f"  {r['date']} {r['ts'][11:16]}UTC views={r['views']:>5} slogan={has_slogan} | ...{tail}")
print(f"SLOGAN in last 15 drey reels: {slogan_count}/15")

# Drey statics
drey_stats = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'False' and not is_story(r)]
drey_stats.sort(key=lambda r: r['ts'])
print(f"Drey feed statics in csv: n={len(drey_stats)}")
for r in drey_stats[-6:]:
    print(f"  {r['date']} {r['ts'][11:16]}UTC views={r['views']} theme={r['theme']} | {r['content'][:70]}")

# Kevin statics by 17-20 ET window
kev_stats_30 = []
for r in rows:
    if r['account'] == 'kevin_ig' and r['is_reel'] == 'False' and not is_story(r) and r['date'] >= '2026-10-25':
        try:
            t = datetime.datetime.strptime(r['ts'][:19].replace('T', ' '), '%Y-%m-%d %H:%M:%S')
        except Exception:
            continue
        et_hour = (t - datetime.timedelta(hours=5)).hour
        try:
            v = float(r['views'])
        except Exception:
            continue
        kev_stats_30.append((et_hour, v, r['date']))
eve = [v for h, v, d in kev_stats_30 if 17 <= h <= 20]
aft = [v for h, v, d in kev_stats_30 if h == 14]
print(f"Kevin statics 30d: 17-20 ET n={len(eve)} values={sorted(eve)} med={statistics.median(eve) if eve else None}")
print(f"Kevin statics 30d: 14 ET n={len(aft)} values={sorted(aft)} med={statistics.median(aft) if aft else None}")

# Kevin top reels all time (for rank check of the room reel)
kev_reels_all = [(float(r['views']), r['date'], r['url']) for r in rows
                 if r['account'] == 'kevin_ig' and r['is_reel'] == 'True' and not is_story(r)
                 and r['views'] not in ('', None)]
kev_reels_all.sort(reverse=True)
print("Kevin top 5 reels all-time (csv, may lag today's climb):")
for v, d, u in kev_reels_all[:5]:
    print(f"  {v:>7.0f} {d} {u}")

# Drey reels top 30d
drey_reels_30 = [(float(r['views']), r['date']) for r in drey_reels if r['date'] >= '2026-10-25']
drey_reels_30.sort(reverse=True)
print("Drey top 5 reels 30d:", [(f'{v:.0f}', d) for v, d in drey_reels_30[:5]])
