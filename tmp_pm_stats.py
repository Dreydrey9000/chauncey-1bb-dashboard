import csv, io, os
from collections import defaultdict

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
with open(path, newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

def med(vals):
    v = sorted(vals); n = len(v)
    if not v: return None
    return v[n//2] if n % 2 else (v[n//2-1] + v[n//2]) / 2

print("total rows:", len(rows))
for acct in ['drey_ig', 'kevin_ig']:
    for reel in ['True', 'False']:
        sub = [r for r in rows if r['account'] == acct and r['is_reel'] == reel and r['theme'] not in ('other', '')]
        views = [float(r['views'] or 0) for r in sub]
        print(f"{acct} {'REEL' if reel=='True' else 'STATIC'} n={len(sub)} median_views={med(views)}")
    th = defaultdict(list)
    for r in rows:
        if r['account'] == acct and r['theme'] not in ('other', ''):
            th[(r['theme'], r['is_reel'])].append(float(r['views'] or 0))
    print(acct, "themes:")
    for (theme, reel), v in sorted(th.items(), key=lambda x: -(med(x[1]) or 0)):
        print(f"  {theme} {'reel' if reel=='True' else 'static'}: n={len(v)} median={med(v)}")

# last 3 posts per founder (non-story)
print("\nLast posts per founder:")
for acct in ['drey_ig', 'kevin_ig']:
    sub = [r for r in rows if r['account'] == acct and 'stories/' not in (r['url'] or '')]
    for r in sub[-4:]:
        print(acct, r['date'], r['ts'], 'views=', r['views'], 'theme=', r['theme'], 'reel=', r['is_reel'], 'er=', r['er'], 'url=', r['url'])
