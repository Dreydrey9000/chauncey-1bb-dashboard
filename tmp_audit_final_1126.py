# Inspire-brief PM FINAL AUDIT — 2026-11-26 evening.
# Independent re-derivation of every quoted claim, using FULL captions (CSV content is full;
# pm_delta captions are truncated at 120 chars — known artifact). Prints PASS/FAIL per claim.
import csv, json, statistics
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))
fresh = json.load(open(BASE + '/raw/pm_delta_2026-11-26.json'))['fresh']
SLOGAN = 'Follow for AI systems'

# Full captions for today's 2 fresh reels (from Zernio full pull, printed in tmp_pm_stats2 run):
full_fresh = {
    'https://www.instagram.com/reel/DgNmOF_hrLs': "You're already stretched thin... What would you do with the hours posting takes from you now? Follow for AI systems instead of hiring an employee.",
    'https://www.instagram.com/reel/DgLxSX2B13h': "You're the bottleneck... What's the most robotic thing you still do every week? Follow for AI systems instead of hiring an employee.",
}
reels = []
for r in rows:
    if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and '/reel/' in str(r.get('url', '')) and '/stories/' not in str(r.get('url', '')):
        reels.append({'ts': r['ts'], 'url': r['url'].rstrip('/'), 'content': str(r.get('content') or ''), 'comments': r.get('comments')})
seen = {r['url'] for r in reels}
for p in fresh['drey_ig']:
    u = str(p.get('url', '')).rstrip('/')
    if '/reel/' in u and u not in seen:
        reels.append({'ts': p.get('posted_at'), 'url': u, 'content': full_fresh.get(u, str(p.get('caption') or '')), 'comments': p.get('comments')})
reels.sort(key=lambda r: str(r['ts']), reverse=True)

n18 = reels[:18]
s18 = sum(1 for r in n18 if SLOGAN in r['content'])
n19 = reels[:19]
s19 = sum(1 for r in n19 if SLOGAN in r['content'])
z19 = sum(1 for r in n19 if str(r['comments']) in ('0', '0.0', '', 'None'))
print(f'CLAIM slogan streak: 17 of last 18 -> actual {s18} of {len(n18)}:', 'PASS' if s18 == 17 else 'FAIL')
print(f'CLAIM zero-comments: 19 of last 19 -> actual {z19} of {len(n19)}:', 'PASS' if z19 == 19 else 'FAIL')
print(f'(context: slogan on last 19 = {s19} of 19)')

med = statistics.median([int(float(r.get('views') or 0)) for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and '/reel/' in str(r.get('url', '')) and '/stories/' not in str(r.get('url', ''))])
print(f'CLAIM Drey reel median 179 (n=53) -> actual {repr(med)} (n={len(reels)}):', 'PASS' if med == 179 and len(reels) == 53 else 'FAIL')
print(f'CLAIM 152/179 = 85% -> {round(152/179*100)}%')

# Kevin claims
krows = [r for r in rows if r['account'] == 'kevin_ig' and '/stories/' not in str(r.get('url', ''))]
kreels = [int(float(p['views'] or 0)) for p in krows if p['is_reel'] == 'True' and '/reel/' in str(p.get('url', ''))]
kstatics = [int(float(p['views'] or 0)) for p in krows if p['is_reel'] == 'False' and '/p/' in str(p.get('url', ''))]
print(f'CLAIM Kevin reel median 874.0 (n=68) -> {repr(statistics.median(kreels))} (n={len(kreels)}):', 'PASS' if statistics.median(kreels) == 874.0 and len(kreels) == 68 else 'FAIL')
print(f'CLAIM Kevin statics median 1984 (n=67) -> {repr(statistics.median(kstatics))} (n={len(kstatics)}):', 'PASS' if statistics.median(kstatics) == 1984 and len(kstatics) == 67 else 'FAIL')

# room/volleyball numbers from fresh
room = next((p for p in fresh['kevin_ig'] if 'DgIUQyCjMAT' in str(p.get('url'))), None)
volley = next((p for p in fresh['kevin_ig'] if 'DgGfPVaEnw2' in str(p.get('url'))), None)
print(f'CLAIM room reel 6,859 + volleyball 6,686 -> {room["views"]} / {volley["views"]}:', 'PASS' if room['views'] == 6859 and volley['views'] == 6686 else 'FAIL')
print(f'CLAIM comment rates 0.03% vs 0.10% -> bedros {round(53/173160*100, 3)}%, room {round(7/6859*100, 3)}%')

# Drey statics
dstatics = [int(float(r['views'] or 0)) for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'False' and '/p/' in str(r.get('url', ''))]
print(f'CLAIM Drey statics median 414.0 (n=8) -> {repr(statistics.median(dstatics))} (n={len(dstatics)}):', 'PASS' if statistics.median(dstatics) == 414.0 and len(dstatics) == 8 else 'FAIL')
print(f'CLAIM 414.0/179 = 2.3x -> {round(414.0/179, 1)}x')
