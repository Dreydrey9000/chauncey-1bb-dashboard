# Inspire-brief stats helper — evening edition 2026-11-26 PM.
# Prints exact medians (repr, no int() truncation) from posts_all.csv + fresh pm_delta overlay.
# Output is quoted directly in the brief → print with explicit formatting.
import csv, json, statistics, datetime, re
from collections import defaultdict

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))
print('cols:', list(rows[0].keys()))

def load(prefix):
    out = []
    for r in rows:
        if r['account'] == prefix:
            out.append(r)
    return out

def fmt(x):
    return repr(x)

def stats_for(posts, label):
    vs = []
    for p in posts:
        try:
            vs.append(int(float(p['views'] or 0)))
        except Exception:
            pass
    med = statistics.median(vs) if vs else None
    print(f'{label}: n={len(vs)} median={fmt(med)}')
    return med

print('=== DREY IG (posts_all.csv, 6:31a snapshot) ===')
drey = load('drey_ig')
drey_reels = [p for p in drey if '/reel/' in p.get('url', '') or p.get('post_type') == 'reel']
drey_statics = [p for p in drey if '/p/' in p.get('url', '') or p.get('post_type') == 'static']
# fallback: infer from URL
if not drey_reels and not drey_statics:
    drey_reels = [p for p in drey if '/reel/' in str(p.get('url', ''))]
    drey_statics = [p for p in drey if '/p/' in str(p.get('url', ''))]
stats_for(drey, 'all posts')
stats_for(drey_reels, 'reels only (by URL)')
stats_for(drey_statics, 'statics only (by URL)')

print()
print('=== KEVIN IG (posts_all.csv, 6:31a snapshot) ===')
kevin = load('kevin_ig')
kevin_reels = [p for p in kevin if '/reel/' in str(p.get('url', ''))]
kevin_statics = [p for p in kevin if '/p/' in str(p.get('url', ''))]
stats_for(kevin, 'all posts')
stats_for(kevin_reels, 'reels only (by URL)')
stats_for(kevin_statics, 'statics only (by URL)')

# Kevin statics by posting window (hour in ET from date field)
print()
print('=== KEVIN statics by ET hour window ===')
def hour_et(p):
    d = str(p.get('date', ''))
    m = re.match(r'(\d{4}-\d{2}-\d{2})[T ](\d{2}):(\d{2})', d)
    if not m:
        return None
    dt = datetime.datetime(int(m.group(1)[:4]), int(m.group(1)[5:7]), int(m.group(1)[8:10]), int(m.group(2)), int(m.group(3)))
    # date is already ET per dashboard convention
    return dt.hour
byw = defaultdict(list)
for p in kevin_statics:
    h = hour_et(p)
    if h is None:
        continue
    if 16 <= h or h < 21:  # 4p-8:59p window approximation
        pass
    w = None
    if 13 <= h < 16:
        w = '1-4p'
    elif 16 <= h < 21:
        w = '4-9p'
    else:
        w = 'other'
    try:
        byw[w].append(int(float(p['views'] or 0)))
    except Exception:
        pass
for w, vs in sorted(byw.items()):
    print(f'{w}: n={len(vs)} median={fmt(statistics.median(vs))} mean={fmt(round(sum(vs)/len(vs), 1))}')

print()
print('=== FRESH OVERLAY (pm_delta_2026-11-26.json — Zernio REST pull ~6p ET) ===')
fresh = json.load(open(BASE + '/raw/pm_delta_2026-11-26.json'))['fresh']

today = '2026-11-26'
for acc in ('drey_ig', 'kevin_ig'):
    posts = fresh[acc]
    feed = [p for p in posts if '/stories/' not in str(p.get('url', ''))]
    print(f'--- {acc}: {len(feed)} FEED posts (stories excluded)')
    for p in feed:
        date = str(p.get('posted_at', ''))[:10]
        ts = str(p.get('posted_at', ''))
        print(f"  {ts} | views={p.get('views')} likes={p.get('likes')} comments={p.get('comments')} | {str(p.get('caption'))[:60]!r} | {p.get('url')}")

# overlay fresh onto CSV rows for all-time top-N
print()
print('=== Kevin all-time reel top-5 (CSV + fresh overlay) ===')
merged = defaultdict(dict)
for p in kevin_reels:
    try:
        merged[p['url'].rstrip('/')]['csv'] = int(float(p['views'] or 0))
    except Exception:
        pass
for p in fresh['kevin_ig']:
    u = str(p.get('url', '')).rstrip('/')
    if '/reel/' in u and p.get('views') is not None:
        try:
            merged[u]['fresh'] = int(p['views'])
        except Exception:
            pass
top = sorted(((max(d.get('csv', 0), d.get('fresh', 0)), u) for u, d in merged.items()), reverse=True)[:5]
for v, u in top:
    print(f'  {v} {u}')
