# Final audit 2026-11-26 AM: recompute EVERY number quoted in the brief from this run's sources
import json, csv, statistics
from datetime import datetime

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
am = json.load(open(f'{BASE}/raw/am_delta_2026-11-26.json'))['fresh']
rows = list(csv.DictReader(open(f'{BASE}/posts_all.csv')))

def feed(r):
    return r['content'].strip() != '' and '/stories/' not in r['url']

def num(r):
    try:
        return float(r['views'])
    except (ValueError, TypeError):
        return None

def hour_utc(r):
    try:
        return datetime.fromisoformat(r['ts']).hour
    except Exception:
        return None

# --- lookalike counts (this run's tokscript_pull stdout values) ---
rowan6 = [29191, 64793, 82107, 63661, 34059, 17075]
print('rowan: 5 of 6 in 29k-82k =', sum(1 for v in rowan6 if 29000 <= v <= 82107), 'of', len(rowan6))
print('rowan overnight: 16028 -> 29191 =', f'+{100*(29191/16028-1):.0f}%')

gerard12 = [135335, 128473, 1982, 128258, 105316, 111115, 123664, 129895, 98618, 136629, 8822, 965]
print('gerard: 9 of 12 in 98k-158k =', sum(1 for v in gerard12 if 98000 <= v <= 158000), 'of', len(gerard12))

bedros = [256031, 233220, 187912, 227156, 387801, 183675, 214557, 77298]
streak = 0
for v in bedros:
    if v >= 180000:
        streak += 1
    else:
        break
print('bedros: straight 180k+ =', streak)

# --- Drey slogan check from FULL captions (am_delta) ---
drey_reels = [p for p in am['drey_ig'] if '/reel/' in (p['url'] or '')]
slogan = [p for p in drey_reels if (p['caption'] or '').rstrip().endswith('Follow for AI systems instead of hiring an employee.')]
print('Drey reels in 3d pull:', len(drey_reels), '| ending with slogan:', len(slogan),
      '| comments total:', sum(p['comments'] or 0 for p in drey_reels))
for p in drey_reels:
    print('   ', p['posted_at'], p['views'], 'com=', p['comments'],
          'slogan' if (p['caption'] or '').rstrip().endswith('Follow for AI systems instead of hiring an employee.') else 'NO-SLOGAN')

# --- Drey climb + rank ---
noon = [p for p in am['drey_ig'] if 'DgLBOOBh3nn' in p['url']][0]
print('Drey noon reel: 244 ->', noon['views'], f"= +{100*(noon['views']/244-1):.0f}%")

drey_feed = [r for r in rows if r['account'] == 'drey_ig' and feed(r)]
ai_since = sorted([num(r) for r in drey_feed if r['is_reel'] == 'True' and r['theme'] == 'ai_systems'
                   and num(r) is not None and r['date'] >= '2026-11-12'], reverse=True)
rank = ai_since.index(noon['views']) + 1 if noon['views'] in ai_since else '?'
print('Drey ai_systems reels since 11-12 top5:', ai_since[:5], '| noon reel rank:', rank, 'of', len(ai_since))

drey_noon_slot = [num(r) for r in drey_feed if hour_utc(r) in (17, 18) and num(r) is not None]
drey_stat = [num(r) for r in drey_feed if r['is_reel'] == 'False' and num(r) is not None]
drey_r30 = [num(r) for r in drey_feed if r['is_reel'] == 'True' and num(r) is not None and r['date'] >= '2026-10-27']
print(f'Drey noon-slot(12-1p ET) median={statistics.median(drey_noon_slot)} n={len(drey_noon_slot)}')
print(f'Drey statics median={statistics.median(drey_stat)} n={len(drey_stat)} | reels 30d median={statistics.median(drey_r30)} n={len(drey_r30)}')

# --- Kevin ---
kev_feed = [r for r in rows if r['account'] == 'kevin_ig' and feed(r)]
kst = [r for r in kev_feed if r['is_reel'] == 'False' and num(r) is not None]
early = [num(r) for r in kst if hour_utc(r) in (18, 19, 20)]     # 1-4p ET
eve = [num(r) for r in kst if hour_utc(r) in (21, 22, 23, 0, 1)] # 4-9p ET
kident = [num(r) for r in kst if r['theme'] == 'identity']
kroom_st = [num(r) for r in kst if r['theme'] == 'room']
print(f'Kevin statics 1-4p ET median={int(statistics.median(early)):,} n={len(early)} | 4-9p ET median={int(statistics.median(eve)):,} n={len(eve)}')
print(f'Kevin identity statics median={int(statistics.median(kident)):,} n={len(kident)} | room statics median={int(statistics.median(kroom_st)):,} n={len(kroom_st)}')

room = [p for p in am['kevin_ig'] if 'DgIUQyCjMAT' in p['url']][0]
vb = [p for p in am['kevin_ig'] if 'DgGfPVaEnw2' in p['url']][0]
ident = [p for p in am['kevin_ig'] if 'DgLOx8wEeIk' in p['url']][0]
print(f"Kevin room reel {room['views']} (com={room['comments']}, likes={room['likes']}) vs volleyball {vb['views']} -> room is #1: {room['views'] > vb['views']}")
print(f"room climb 6429 -> {room['views']} = +{100*(room['views']/6429-1):.0f}% | volleyball 6513 -> {vb['views']} = +{100*(vb['views']/6513-1):.0f}%")
print(f"identity static 417 -> {ident['views']} in 13h = +{100*(ident['views']/417-1):.0f}%")
# is room reel #1 among all Kevin reels ever (CSV)?
k_reels = sorted([num(r) for r in kev_feed if r['is_reel'] == 'True' and num(r) is not None], reverse=True)
print('Kevin top reels all-time (CSV):', [int(v) for v in k_reels[:3]])
# hours since identity static posted (19:00 UTC 11-25 = 2p ET) — pulled 12:05 UTC = 7:05a ET
print('identity static age at pull: ~13h (posted 2p ET 11-25, pulled 7:05a ET 11-26)')
