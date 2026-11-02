# 2026-11-02 AM: exact 7-day medians + lookalike deltas (all arithmetic in code, not head)
import csv, statistics
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
def iv(s):
    try: return int(float((s or '').strip()))
    except: return None
for r in rows:
    r['v'] = iv(r.get('views')); r['d'] = r.get('date','')
    r['reel'] = str(r.get('is_reel','')).lower()=='true'

# 7-day window ending yesterday (2026-11-01)
lo, hi = '2026-10-26', '2026-11-01'
for acc in ('drey_ig','kevin_ig'):
    for kind, want in (('reel', True), ('static', False)):
        vs = [r['v'] for r in rows if r['account']==acc and r['reel']==want and r['v'] is not None and lo<=r['d']<=hi]
        if vs:
            print(f'{acc} {kind} 7d median {statistics.median(vs):.0f} n={len(vs)} sorted={sorted(vs)}')

# Drey zero-post check Sat+Sun
for acc in ('drey_ig','kevin_ig'):
    sat = [r['v'] for r in rows if r['account']==acc and r['d']=='2026-10-31']
    sun = [r['v'] for r in rows if r['account']==acc and r['d']=='2026-11-01']
    print(f'{acc} sat={sorted(sat)} sun={sorted(sun)}')

# lookalike deltas (vs Saturday 6p ET read from inspire.js 2026-10-31 PM)
print('liam gate: now 17016 vs 15135 =', f'{(17016-15135)/15135*100:+.1f}%', '| comments 311 vs 270 =', f'{(311-270)/270*100:+.1f}%')
print('drey email reel final 123 vs 7d median')
print('kevin AI-take 180, over-deliver 791 vs reel median above')
print('kevin identity reel 1543 vs transformation 1384')
# combined Ryan session views (two 10-27 reels)
ry = [r['v'] for r in rows if r['account']=='drey_ig' and r['d']=='2026-10-27']
print('drey 10-27 Ryan reels:', ry, 'sum', sum(ry))
# kevin identity reel vs room reel Sunday
print('meltzer pick 3301 views 113 likes =', f'{113/3301*100:.1f}%', 'like rate')
