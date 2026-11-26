# Morning inspire-brief stats (2026-11-26 AM) — quotes must come from THIS script only
import json, csv, statistics

# 1) Lookalike medians from THIS run's pull (stdout already saved by cron operator)
# Manually transcribed from tokscript_pull.py output of this run (2026-11-26 07:00 ET):
pull = {
    'liamottley': [
        ('2026-11-19', 14408), ('2026-10-31', 19045), ('2026-10-29', 12561),
        ('2026-10-21', 13640), ('2026-10-11', 30107), ('2026-10-07', 12688),
        ('2026-10-04', 11062), ('2026-10-03', 17329), ('2026-10-02', 13954),
        ('2026-09-27', 10691), ('2026-09-26', 21657), ('2026-09-25', 31820),
    ],
    'rowancheung': [
        ('2026-11-25', 29191), ('2026-11-24', 64793), ('2026-11-23', 82107),
        ('2026-11-21', 63661), ('2026-11-20', 34059), ('2026-11-19', 17075),
        ('2026-11-18', 117037), ('2026-11-17', 39082), ('2026-11-13', 426044),
    ],
    'bedroskeuilian': [
        ('2026-11-24', 256031), ('2026-11-22', 233220), ('2026-11-19', 187912),
        ('2026-11-16', 227156), ('2026-11-12', 387801), ('2026-11-11', 183675),
        ('2026-11-09', 214557), ('2026-11-06', 77298), ('2026-11-04', 167511),
        ('2026-11-03', 157014), ('2026-11-02', 364093), ('2026-10-30', 206579),
    ],
    'gerardadams': [
        ('2026-11-24', 135335), ('2026-11-23', 128473), ('2026-11-21', 1982),
        ('2026-11-20', 128258), ('2026-11-20', 105316), ('2026-11-19', 111115),
        ('2026-11-18', 123664), ('2026-11-18', 129895), ('2026-11-17', 98618),
        ('2026-11-16', 136629), ('2026-11-14', 8822), ('2026-11-12', 965),
    ],
}

print('== LOOKALIKE MEDIANS (this run) ==')
for u, rows in pull.items():
    views = [v for _, v in rows]
    last7 = [v for d, v in rows if d >= '2026-11-19']
    print(f'{u}: n={len(rows)} median_all={int(statistics.median(views)):,} '
          f'fresh_n={len(last7)} median_fresh={int(statistics.median(last7)) if last7 else "n/a":,}')

# 2) Founder stats from posts_all.csv (feed only — no /stories/, no empty content)
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

def feed(r):
    return r['content'].strip() != '' and '/stories/' not in r['url']

def num(r, k):
    try:
        return float(r[k])
    except (ValueError, TypeError):
        return None

drey = [r for r in rows if r['account'] == 'drey_ig' and feed(r)]
kevin = [r for r in rows if r['account'] == 'kevin_ig' and feed(r)]
print()
print('== FOUNDER FEED POSTS ==')
print(f'drey_ig feed n={len(drey)}, kevin_ig feed n={len(kevin)}')

def top_theme(account_rows, label, n=3):
    by_theme = {}
    for r in account_rows:
        t = r['theme']
        v = num(r, 'views')
        if v is not None:
            by_theme.setdefault(t, []).append(v)
    stats = []
    for t, vs in by_theme.items():
        stats.append((t, len(vs), int(statistics.median(vs))))
    stats.sort(key=lambda x: -x[2])
    print(f'{label} theme medians (n, median views):')
    for t, c, m in stats[:n]:
        print(f'  {t}: n={c} median={m:,}')

top_theme(drey, 'DREY')
print()
top_theme(kevin, 'KEVIN')

def last7_rows(account_rows):
    return [r for r in account_rows if r['date'] >= '2026-11-19']

for label, ars in (('DREY', drey), ('KEVIN', kevin)):
    recent = last7_rows(ars)
    print(f'{label} last-7d posts (since 11-19): n={len(recent)}')
    for r in sorted(recent, key=lambda r: -num(r, 'views') or 0):
        print(f"  {r['date']} views={int(float(r['views'])):,} likes={r['likes']} com={r['comments']} "
              f"reel={r['is_reel']} theme={r['theme']} | {r['url']}")
        print(f"    {r['content'][:100].replace(chr(10),' ')}")
    print()

# Kevin reels vs statics (all-time, feed only)
kr = [r for r in kevin if r['is_reel'] == 'True']
ks = [r for r in kevin if r['is_reel'] == 'False']
if kr and ks:
    print(f"KEVIN reels median={int(statistics.median([num(r,'views') for r in kr if num(r,'views') is not None])):,} (n={len(kr)}) "
          f"vs statics median={int(statistics.median([num(r,'views') for r in ks if num(r,'views') is not None])):,} (n={len(ks)})")

# All-time top per founder (feed)
for label, ars in (('DREY', drey), ('KEVIN', kevin)):
    best = max(ars, key=lambda r: num(r, 'views') or 0)
    print(f'{label} all-time top feed post: {int(float(best["views"])):,} views | {best["theme"]} | {best["url"]}')

# Drey confession/room vs ai-tool anchors
conf_room = [r for r in drey if r['theme'] in ('confession', 'room')]
ai_sys = [r for r in drey if r['theme'] == 'ai_systems']
print(f"DREY confession+room median={int(statistics.median([num(r,'views') for r in conf_room if num(r,'views') is not None])):,} (n={len(conf_room)}) "
      f"vs ai_systems median={int(statistics.median([num(r,'views') for r in ai_sys if num(r,'views') is not None])):,} (n={len(ai_sys)})")
