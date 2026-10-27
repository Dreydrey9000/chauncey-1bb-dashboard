#!/opt/homebrew/bin/python3
"""Evening 2026-10-27 inspire delta: CSV medians + today rows + fresh Zernio REST (3d)."""
import csv, json, os, statistics, urllib.request, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
FD = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()

rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
print(f'CSV rows: {len(rows)}; max date: {max(r["date"] for r in rows)}; today rows: {sum(1 for r in rows if r["date"] == TODAY)}')

def to_int(v):
    try:
        return int(float(v))
    except Exception:
        return None

def med(label, data):
    vals = [to_int(v) for v in data]
    vals = [v for v in vals if v is not None]
    if vals:
        print(f'  {label}: median={statistics.median(vals):.1f} n={len(vals)}')

print('\n--- DREY IG (all-time CSV) ---')
d = [r for r in rows if r['account'] == 'drey_ig']
med('all', [r['views'] for r in d])
med('reels', [r['views'] for r in d if r['is_reel'] == 'True'])
med('statics', [r['views'] for r in d if r['is_reel'] == 'False'])
for t in ('confession', 'room', 'ai_systems'):
    med(f'theme={t}', [r['views'] for r in d if r['theme'] == t])
print('last 5 drey rows:')
for r in sorted(d, key=lambda r: r['date'], reverse=True)[:5]:
    print(f'  {r["date"]} reel={r["is_reel"]} v={r["views"]} c={r["comments"]} {r["theme"]} | {" ".join((r["content"] or "").split())[:70]}')

print('\n--- KEVIN IG (all-time CSV) ---')
k = [r for r in rows if r['account'] == 'kevin_ig']
med('all', [r['views'] for r in k])
med('statics', [r['views'] for r in k if r['is_reel'] == 'False'])
med('reels', [r['views'] for r in k if r['is_reel'] == 'True'])
for t in ('identity', 'room', 'discipline', 'faith'):
    med(f'theme={t}', [r['views'] for r in k if r['theme'] == t])
print('last 5 kevin rows:')
for r in sorted(k, key=lambda r: r['date'], reverse=True)[:5]:
    print(f'  {r["date"]} reel={r["is_reel"]} v={r["views"]} c={r["comments"]} {r["theme"]} | {" ".join((r["content"] or "").split())[:70]}')

print('\n--- FRESH ZERNIO REST (last 3 days, incl today) ---')
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
for name, aid in (('drey_ig', '6a1c7e1e2b2567671a7f25ee'), ('kevin_ig', '6a1c97b22b2567671a7ff845')):
    url = (f'https://getlate.dev/api/v1/analytics?platform=instagram&accountId={aid}'
           f'&fromDate={FD}&toDate={TODAY}&limit=50&page=1')
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
        posts = resp.get('posts', [])
        print(f'== {name}: {len(posts)} posts {FD}..{TODAY}')
        for p in posts:
            an = p.get('analytics') or {}
            print(f'  {str(p.get("publishedAt"))[:19]} v={an.get("views")} l={an.get("likes")} c={an.get("comments")} | {p.get("platformPostUrl")}')
            print(f'      {" ".join(str(p.get("content") or "").split())[:110]}')
    except Exception as e:
        print(f'== {name}: FAILED {e!r}')
