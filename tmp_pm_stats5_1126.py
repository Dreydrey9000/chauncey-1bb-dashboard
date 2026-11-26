# Inspire-brief PM helper 5 — 2026-11-26 evening. Slogan + comment streaks, exact.
# Merges CSV feed reels with today's fresh reel (12:07p ET, not in 6:31a CSV), dedup by URL.
import csv, json
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))
fresh = json.load(open(BASE + '/raw/pm_delta_2026-11-26.json'))['fresh']

SLOGAN = 'Follow for AI systems'
reels = []
for r in rows:
    if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and '/reel/' in str(r.get('url', '')) and '/stories/' not in str(r.get('url', '')):
        reels.append({'ts': r['ts'], 'url': r['url'].rstrip('/'), 'content': str(r.get('content') or ''), 'comments': r.get('comments')})
seen = {r['url'] for r in reels}
for p in fresh['drey_ig']:
    u = str(p.get('url', '')).rstrip('/')
    if '/reel/' in u and u not in seen:
        reels.append({'ts': p.get('posted_at'), 'url': u, 'content': str(p.get('caption') or ''), 'comments': p.get('comments'), 'fresh': True})
reels.sort(key=lambda r: str(r['ts']), reverse=True)

print('=== last 20 Drey feed reels (merged CSV + fresh, latest first) ===')
for r in reels[:20]:
    has = SLOGAN in r['content']
    print(f"  {r['ts']} slogan={has} comments={r['comments']} {'FRESH' if r.get('fresh') else 'csv  '} {r['url'][-16:]}")

n = 18
last = reels[:n]
slog = sum(1 for r in last if SLOGAN in r['content'])
print(f'last {n} reels: slogan on {slog} of {n}')
n2 = 19
last2 = reels[:n2]
zero = sum(1 for r in last2 if str(r['comments']) in ('0', '0.0', '', 'None'))
print(f'last {n2} reels: zero comments on {zero} of {n2}')
