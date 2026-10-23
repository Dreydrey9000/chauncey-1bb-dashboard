# Own-data medians for 2026-10-23 am brief — grounded post ideas
import csv, statistics, collections, datetime

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
def num(x):
    try: return int(float(x))
    except: return 0

for acct in ('drey_ig','drey_tt','kevin_ig','kevin_tt'):
    sub = [r for r in rows if r['account']==acct and num(r['views'])>0]
    if not sub: continue
    sub.sort(key=lambda r: r['ts'], reverse=True)
    last30 = sub[:30]
    med = statistics.median(num(r['views']) for r in last30)
    print(f"\n== {acct} (n={len(sub)}, last-30-posts median views={med:.0f}) ==")
    for r in last30[:5]:
        print(f"  {r['date']} views={num(r['views']):>6} likes={num(r['likes']):>5} comments={num(r['comments']):>3} reel={r['is_reel']} theme={r['theme'][:30]} | {r['content'][:60].replace(chr(10),' ')}")
    # theme medians on last 30
    by_theme = collections.defaultdict(list)
    for r in last30:
        by_theme[r['theme'] or 'none'].append(num(r['views']))
    tops = sorted(((statistics.median(v), k, len(v)) for k,v in by_theme.items() if len(v)>=2), reverse=True)
    for m,k,n in tops[:5]:
        print(f"  theme median: {k[:35]:35} n={n} median={m:.0f}")
    # reels vs static for kevin
    reels = [num(r['views']) for r in last30 if r['is_reel'].strip().lower() in ('1','true','yes')]
    stats_ = [num(r['views']) for r in last30 if r['is_reel'].strip().lower() not in ('1','true','yes')]
    if reels and stats_:
        print(f"  reels n={len(reels)} median={statistics.median(reels):.0f} | static n={len(stats_)} median={statistics.median(stats_):.0f}")
