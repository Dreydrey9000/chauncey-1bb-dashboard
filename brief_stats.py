# Morning brief: founder CSV medians + gaps (chauncey, 2026-10-02 AM)
import csv, statistics as st
from collections import defaultdict
from datetime import date

rows = list(csv.DictReader(open('posts_all.csv')))
for r in rows:
    r['views'] = int(r['views'] or 0)

print("CSV max date:", max(r['date'] for r in rows))

def med(vals):
    vals = sorted(vals)
    return st.median(vals) if vals else None

for who, prefix in [('DREY', 'drey'), ('KEVIN', 'kevin')]:
    sub = [r for r in rows if r['account'].startswith(prefix) and r['date'] >= '2026-09-02']
    ig = [r for r in sub if r['account'].endswith('_ig')]
    tt = [r for r in sub if r['account'].endswith('_tt')]
    reels = [r for r in ig if r['is_reel'] == 'True']
    statics = [r for r in ig if r['is_reel'] == 'False']
    print(f"\n=== {who} since 9/2 (n={len(sub)}; IG {len(ig)}, TT {len(tt)}) ===")
    print(f"IG reels n={len(reels)} median views={med([r['views'] for r in reels])}")
    print(f"IG statics n={len(statics)} median views={med([r['views'] for r in statics])}")
    themes = defaultdict(list)
    for r in sub:
        themes[r['theme']].append(r['views'])
    for t, v in sorted(themes.items(), key=lambda kv: -med(kv[1])):
        print(f"  theme {t}: n={len(v)} median={med(v)} max={max(v)}")
    print("last 5 posts:")
    for r in sorted(sub, key=lambda r: r['ts'])[-5:]:
        print(f"  {r['date']} {r['account']} reel={r['is_reel']} theme={r['theme']} "
              f"views={r['views']} likes={r['likes']} comments={r['comments']}")

drey_ig = sorted([r for r in rows if r['account'] == 'drey_ig'], key=lambda r: r['ts'])
last_reel = [r for r in drey_ig if r['is_reel'] == 'True'][-1]
print(f"\nDrey last IG reel: {last_reel['date']} ({last_reel['views']} views, "
      f"theme={last_reel['theme']}, url={last_reel['url']})")
print(f"Drey last IG post any kind: {drey_ig[-1]['date']} ({drey_ig[-1]['views']} views)")
print("Days reel-silent to 10/2:",
      (date(2026, 10, 2) - date(*map(int, last_reel['date'].split('-')))).days)
print("Days fully IG-silent to 10/2:",
      (date(2026, 10, 2) - date(*map(int, drey_ig[-1]['date'].split('-')))).days)
for theme in ['room', 'confession', 'ai_systems', 'lifestyle', 'other', 'podcast']:
    v = [int(r['views']) for r in drey_ig
         if r['is_reel'] == 'True' and r['theme'] == theme and r['date'] >= '2026-08-20']
    if v:
        print(f"Drey reels {theme} since 8/20: {sorted(v)}")
kr = [r for r in rows if r['account'] == 'kevin_ig' and r['is_reel'] == 'True'
      and r['date'] >= '2026-09-20' and r['dur_s']]
print("\nKevin reels since 9/20 (dur, views, theme):",
      [(r['dur_s'], r['views'], r['theme']) for r in kr])
kev_tt = sorted([r for r in rows if r['account'] == 'kevin_tt'], key=lambda r: r['ts'])
print("Kevin last posts overall:",
      [(r['date'], r['account'], r['views'], r['theme']) for r in kev_tt[-2:]])
