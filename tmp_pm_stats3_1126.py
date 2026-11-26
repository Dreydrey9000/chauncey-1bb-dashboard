# Inspire-brief PM helper 3 — 2026-11-26 evening. Final quoted numbers only.
import csv, json, statistics
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))

print('=== CSV coverage: max date per account + today rows ===')
for acc in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acc]
    dates = sorted(r['date'] for r in sub)
    print(f'{acc}: n={len(sub)} date range {dates[0]}..{dates[-1]}')
    for dd in ('2026-11-25', '2026-11-26'):
        tod = [r for r in sub if r['date'] == dd]
        print(f'  {dd}: {len(tod)} rows')
        for r in tod:
            print(f"    ts={r['ts']} is_reel={r['is_reel']} views={r['views']} com={r['comments']} | {r['url'][-20:]} | content_tail={str(r['content'])[-60:]!r}")

print()
print('=== is_reel-flag medians (feed only, exclude stories) ===')
for acc in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acc and '/stories/' not in str(r.get('url', ''))]
    for flag, label in (('True', 'REELS'), ('False', 'STATICS')):
        vs = []
        for r in sub:
            if r['is_reel'] == flag:
                try:
                    vs.append(int(float(r['views'] or 0)))
                except Exception:
                    pass
        if vs:
            print(f'{acc} {label}: n={len(vs)} median={repr(statistics.median(vs))}')

print()
print('=== Drey slogan streak (CSV content tail + today fresh captions) ===')
fresh = json.load(open(BASE + '/raw/pm_delta_2026-11-26.json'))['fresh']
slogan = 'Follow for AI systems'
drey_reels_csv = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True']
tail = [r for r in drey_reels_csv if str(r.get('content', '')).strip()][-17:]
csv_hits = sum(1 for r in tail if slogan in str(r.get('content', '')))
print(f'CSV last 17 reels ending w/ slogan in content: {csv_hits} of 17 (content may be full caption)')
# fresh: today's two reels
fr = [p for p in fresh['drey_ig'] if '/reel/' in str(p.get('url', ''))]
fresh_hits = 0
for p in fr[:2]:
    # captions truncated at 120 chars in pm_delta; slogan check needs full text — use counts from full-caption pull (tmp_pm_stats2 output verified both end with slogan)
    print(f"  fresh reel {p['url'][-16:]} views={p.get('views')} (full caption verified in stats2 run)")
fresh_hits = 2  # both today's reels end with the slogan (full captions printed in tmp_pm_stats2_1126.py run)
print(f'today\'s 2 reels with slogan (full-caption pull): {fresh_hits} of 2 -> streak now {csv_hits + fresh_hits} of {len(tail) + 2}')

print()
print('=== Bedros >=170k streak, latest-first order (from this run\'s TokScript pull) ===')
bedros = [173160, 256180, 233629, 187965, 227254, 393498, 183687, 214608, 77315, 167514, 157018, 364102]
streak = 0
for v in bedros:
    if v >= 170000:
        streak += 1
    else:
        break
print(f'streak >=170k: {streak} (streak values: {bedros[:streak]})')
streak180 = 0
for v in bedros:
    if v >= 180000:
        streak180 += 1
    else:
        break
print(f'streak >=180k: {streak180} (values: {bedros[:streak180]})')

print()
print('=== Founder beat/miss arithmetic (this run) ===')
print(f"Drey compute reel (Nov 25 noon, DgLBOOBh3nn): 995 views @ ~28h vs reels median 183.0 -> {round(995/183.0, 1)}x median")
print(f"Drey last-night 7p reel (DgLxSX2B13h): 152 views @ ~23h vs 183.0 -> {round(152/183.0*100)}% of median")
print(f"Drey noon-today reel (DgNmOF_hrLs): 108 views @ ~6h, skip 61.4%, avg watch 4.6s of 28s")
print(f"Kevin identity static (Nov 25 2p, DgLOx8wEeIk): 669 views @ ~28h vs statics median (this run below)")
print(f"Kevin room reel DgIUQyCjMAT: 6,859 = all-time #1 (was 6,686 at 7a -> +{6859-6686} since morning)")

print()
print('=== Rowan aged reel (Drey imitation, recycled) ===')
print(f"DgLJnhnhaS0: 29,191 at 7a -> 35,792 at 6p = +{round((35792-29191)/29191*100, 1)}%")
