# Verify slogan streak + identify the 1,623 AI-lane reel (2026-11-26 AM)
import csv, json
from datetime import datetime

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(f'{BASE}/posts_all.csv')))
am = json.load(open(f'{BASE}/raw/am_delta_2026-11-26.json'))['fresh']

def feed(r):
    return r['content'].strip() != '' and '/stories/' not in r['url']

drey = [r for r in rows if r['account'] == 'drey_ig' and feed(r) and r['is_reel'] == 'True']
drey.sort(key=lambda r: r['ts'], reverse=True)

# overlay fresh views on the newest reels
fresh = {p['url']: p for p in am['drey_ig'] if '/reel/' in (p['url'] or '')}
SLOGAN = 'Follow for AI systems instead of hiring an employee.'
n = 0
slogan_n = 0
com_total = 0
for r in drey[:17]:
    url = r['url']
    cap = fresh[url]['caption'] if url in fresh else r['content']
    v = fresh[url]['views'] if url in fresh else r['views']
    c = fresh[url]['comments'] if url in fresh else r['comments']
    n += 1
    has = cap.rstrip().endswith(SLOGAN)
    slogan_n += has
    com_total += int(float(c or 0))
    if n <= 6:
        print(f"{r['ts'][:16]} v={v} com={c} slogan={has} theme={r['theme']}")
print(f'LAST {n} REELS: slogan-ending = {slogan_n} of {n}; total comments = {com_total}')

# the 1623 reel identity
for r in drey:
    if r['views'] and float(r['views']) == 1623:
        print('1623 reel:', r['ts'], r['theme'], r['url'])
        print('   caption tail:', r['content'][-120:].replace('\n', ' '))

# noon-slot history for context (12p ET = 17-18 UTC)
noon = [(r['ts'][:10], int(float(fresh[r['url']]['views'] if r['url'] in fresh else r['views'] or 0))) for r in drey if datetime.fromisoformat(r['ts']).hour in (17, 18)]
noon.sort(reverse=True)
print('noon-slot reels (date, views):', noon[:8])
