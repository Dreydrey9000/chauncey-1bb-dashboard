# Inspire-brief PM helper 2 — 2026-11-26 evening.
# 1) Show latest CSV rows per founder (coverage vs today)
# 2) Pull FULL captions for today's Drey posts (slogan check) via Zernio REST
# 3) Compute deltas/streaks quoted in the brief
import csv, json, urllib.request, datetime, statistics
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))

print('=== latest 4 CSV rows per founder account ===')
for acc in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acc]
    for r in sub[:4]:
        print(f"  {acc} | ts={r['ts']} date={r['date']} is_reel={r['is_reel']} views={r['views']} | {r['url']}")

print()
print('=== CSV date column sample formats ===')
for r in rows[:3] + [r for r in rows if r['account'] == 'kevin_ig'][:2]:
    print(f"  ts={r['ts']!r} date={r['date']!r}")

print()
print('=== FULL captions for Drey today (Zernio REST, no truncation) ===')
KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
API = 'https://getlate.dev/api/v1'
def get(path):
    req = urllib.request.Request(f'{API}/{path}', headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())
d = get('analytics?platform=instagram&accountId=6a1c7e1e2b2567671a7f25ee&fromDate=2026-11-26&toDate=2026-11-26&limit=50&page=1')
for p in d.get('posts', []):
    print('---', p.get('publishedAt'), p.get('platformPostUrl'))
    print(str(p.get('content') or ''))
    print('   analytics:', json.dumps(p.get('analytics') or {}))

print()
print('=== quoted arithmetic ===')
r0, r1 = 29191, 35792
print(f"rowan reel 7a->6p: {r0} -> {r1} = +{round((r1-r0)/r0*100,1)}%")
bedros = [364102,157018,167514,77315,214608,183687,393498,227254,187965,233629,256180,173160]
streak = 0
for v in bedros:
    if v >= 170000: streak += 1
    else: break
print(f"bedros reels >=170k streak from latest: {streak} (values: {bedros[:streak]})")
vs = [14476,19053,12575,13652,30136,12699,11071,17338,13961,10692,21661,31828]
print(f"liam median of last 12: {statistics.median(sorted(vs))}")
