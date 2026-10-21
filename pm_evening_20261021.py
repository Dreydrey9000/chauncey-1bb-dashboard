#!/usr/bin/env python3
"""Evening 2026-10-21: CSV medians + today-dated rows + Kevin full caption (Zernio REST)."""
import csv, json, os, statistics, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = '2026-10-21'

rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
print(f'CSV rows total: {len(rows)}; max date: {max(r["date"] for r in rows)}')
today_rows = [r for r in rows if r['date'] == TODAY]
print(f'Rows dated {TODAY}: {len(today_rows)}')
for r in today_rows:
    print(f'  {r["account"]} {r["date"]} views={r["views"]} theme={r["theme"]} | {r["content"][:60]}')

def med(label, data):
    vals = [int(float(v)) for v in data if v not in ('', None)]
    if vals:
        print(f'{label}: median={statistics.median(vals):.1f} n={len(vals)}')

drey_ig = [r for r in rows if r['account'] == 'drey_ig']
kevin_ig = [r for r in rows if r['account'] == 'kevin_ig']
print('\n--- DREY IG ---')
med('all posts', [r['views'] for r in drey_ig])
med('reels', [r['views'] for r in drey_ig if r['is_reel'] == 'True'])
med('statics', [r['views'] for r in drey_ig if r['is_reel'] == 'False'])
for theme in ('confession', 'room', 'ai'):
    med(f'reels theme={theme}', [r['views'] for r in drey_ig if r['is_reel'] == 'True' and r['theme'] == theme])
print('last 3 drey rows:')
for r in drey_ig[-3:]:
    print(f'  {r["date"]} reel={r["is_reel"]} theme={r["theme"]} views={r["views"]} | {r["content"][:50]}')

print('\n--- KEVIN IG ---')
med('all posts', [r['views'] for r in kevin_ig])
med('statics', [r['views'] for r in kevin_ig if r['is_reel'] == 'False'])
med('reels', [r['views'] for r in kevin_ig if r['is_reel'] == 'True'])
for theme in ('identity', 'room', 'faith'):
    med(f'statics theme={theme}', [r['views'] for r in kevin_ig if r['is_reel'] == 'False' and r['theme'] == theme])
print('last 3 kevin rows:')
for r in kevin_ig[-3:]:
    print(f'  {r["date"]} reel={r["is_reel"]} theme={r["theme"]} views={r["views"]} | {r["content"][:50]}')

print('\n--- KEVIN FULL CAPTION (fresh, today) ---')
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
url = ('https://getlate.dev/api/v1/analytics?platform=instagram'
       '&accountId=6a1c97b22b2567671a7ff845&fromDate=2026-10-21&toDate=2026-10-21&limit=50&page=1')
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
d = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
for p in d.get('posts', []):
    an = p.get('analytics') or {}
    print(p.get('platformPostUrl'), '| views', an.get('views'), '| likes', an.get('likes'))
    print('FULL CAPTION:', p.get('content'))
