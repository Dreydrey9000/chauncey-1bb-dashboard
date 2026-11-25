#!/usr/bin/env python3
"""PM 2026-11-25: beat/miss + slot math computed from THIS run's pull + posts_all.csv."""
import csv, json, datetime, statistics
from collections import defaultdict

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
CSV = BASE + '/posts_all.csv'
FRESH = json.load(open(BASE + '/raw/pm_delta_2026-11-25.json'))['fresh']
NOW = datetime.datetime(2026, 11, 25, 23, 5)  # approx fetch time UTC
TODAY = '2026-11-25'

def is_story(r):
    return '/stories/' in r['url'] or not r['content'].strip()

def feed(acct):
    out = []
    for r in csv.DictReader(open(CSV, newline='', encoding='utf-8')):
        if r['account'] != acct or is_story(r):
            continue
        try:
            v = float(r['views'])
        except (TypeError, ValueError):
            continue
        out.append((v, r))
    out.sort(key=lambda p: p[1]['ts'])
    return out

def med(vals):
    return statistics.median(vals) if vals else None

def ets(ts):
    """ts like '2026-11-25T00:03:21.000Z' or csv '2026-11-25 00:03:21+00:00' -> ET datetime"""
    t = ts.replace('T', ' ').replace('Z', '').replace('+00:00', '').strip()
    dt = datetime.datetime.strptime(t[:19], '%Y-%m-%d %H:%M:%S')
    return dt - datetime.timedelta(hours=5)

print('######## FOUNDER TODAY (Nov 25) ########')
for key in ('drey_ig', 'kevin_ig'):
    print('==', key)
    for p in FRESH[key]:
        u = p['url'] or ''
        if '/stories/' in u:
            continue
        dt = ets(p['posted_at'])
        day = dt.date().isoformat()
        ageh = (NOW - dt).total_seconds() / 3600
        is_reel = '/reel/' in u
        tag = 'REEL' if is_reel else 'STAT'
        print(f"  {day} {dt.strftime('%a %I:%M%p ET')} {tag} age={ageh:.1f}h views={p['views']} likes={p['likes']} com={p['comments']} | {u}")
        print(f"     cap: {p['caption'][:100]}")

print()
print('######## MEDIANS (posts_all.csv, 30d feed-only) ########')
for acct in ('drey_ig', 'kevin_ig'):
    f = feed(acct)
    f30 = [(v, r) for v, r in f if r['date'] >= '2026-10-25']
    reels = [v for v, r in f30 if r['is_reel'] == 'True']
    stats_ = [v for v, r in f30 if r['is_reel'] == 'False']
    print(f"{acct}: 30d reels n={len(reels)} med={med(reels)} | statics n={len(stats_)} med={med(stats_)}")
    if acct == 'drey_ig':
        ai14 = [v for v, r in f30 if r['theme'] == 'ai_systems' and r['is_reel'] == 'True' and r['date'] >= '2026-11-10']
        print(f"  drey AI-lane reels 14d: n={len(ai14)} med={med(ai14)} max={max(ai14)}")
        # slot analysis: ET hour for settled AI-lane reels since Nov 18
        print('  drey AI-lane reels since Nov 18 by ET hour:')
        byhour = defaultdict(list)
        for v, r in f:
            if r['theme'] == 'ai_systems' and r['is_reel'] == 'True' and r['date'] >= '2026-11-18':
                h = ets(r['ts']).hour
                byhour[h].append(v)
        for h, vs in sorted(byhour.items()):
            print(f"    {h:02d}:00 ET hour: n={len(vs)} med={med(vs)} values={sorted(vs)}")
    if acct == 'kevin_ig':
        print('  kevin statics 30d by ET hour:')
        byhour = defaultdict(list)
        for v, r in f30:
            if r['is_reel'] == 'False':
                byhour[ets(r['ts']).hour].append((v, r['date']))
        for h, vs in sorted(byhour.items()):
            print(f"    {h:02d}:00 ET hour: n={len(vs)} med={med([v for v, _ in vs])} max={max(v for v, _ in vs)}")

print()
print('######## CSV ts spot-check (timezone ground truth) ########')
for r in csv.DictReader(open(CSV, newline='', encoding='utf-8')):
    if r['url'] and ('DgIUQyCjMAT' in r['url'] or 'DgGfPVaEnw2' in r['url'] or 'DgIrvbfgPex' in r['url'] or 'DgGn4PqjmNX' in r['url']):
        print(f"  {r['account']} ts={r['ts']} date={r['date']} views={r['views']} {r['url']}")

print()
print('######## LOOKALIKE CLAIMS (this run pull) ########')
LK = json.load(open(BASE + '/pm_look_20261125.json'))
# rowan
row = LK['rowancheung']['reels']
fresh_today = [x for x in row if str(x['date']).startswith(TODAY)]
print(f"rowan: total pulled={len(row)}, posted today={len(fresh_today)}")
for x in fresh_today:
    print('   today reel:', x['date'], x['views'], x['likes'], x['comments'], x['url'])
nov = [x for x in row if str(x['date']).startswith('2026-11')]
vs = sorted(int(x['views']) for x in nov)
print(f"   Nov reels n={len(nov)} med={med(vs)} min={min(vs)} max={max(vs)}")
# bedros
bed = LK['bedroskeuilian']['reels']
streak = 0
for x in bed:
    if int(x['views']) >= 180000:
        streak += 1
    else:
        break
newest_bed = bed[0]
print(f"bedros: 180k+ streak={streak}, newest={newest_bed['date']} views={newest_bed['views']} com={newest_bed['comments']} {newest_bed['url']}")
posted_today_bed = [x for x in bed if str(x['date']).startswith(TODAY)]
print(f"   posted today={len(posted_today_bed)}")
# gerard
ger = LK['gerardadams']['reels']
inband = sum(1 for x in ger[:12] if 98000 <= int(x['views']) <= 158000)
print(f"gerard: last 12 in 98k-158k band = {inband} of 12; newest={ger[0]['date']} views={ger[0]['views']} com={ger[0]['comments']} {ger[0]['url']}")
posted_today_ger = [x for x in ger if str(x['date']).startswith(TODAY)]
print(f"   posted today={len(posted_today_ger)}")
# liam
lia = LK['liamottley']['reels']
last = lia[0]['date']
print(f"liam: newest={last}, silent since Nov 19 = {(datetime.datetime(2026,11,25) - datetime.datetime(2026,11,19)).days} days; posted today={sum(1 for x in lia if str(x['date']).startswith(TODAY))}")
# meltzer
mel = LK['davidmeltzer']['reels']
mel_today = [x for x in mel if str(x['date']).startswith(TODAY)]
print(f"meltzer: posted today={len(mel_today)}")
for x in mel_today:
    print('   today:', x['date'], x['views'], x['likes'], x['comments'], x['url'])
