# Evening delta check: today's founder posts vs medians (cron-safe temp script)
import csv, statistics

rows = list(csv.DictReader(open('posts_all.csv')))
today = '2026-10-14'

def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

# --- today's posts ---
todays = [r for r in rows if r['date'] == today]
print('=== posts dated', today, ':', len(todays), '===')
for r in todays:
    print(f"{r['account']} | reel={r['is_reel']} | views={r['views']} | likes={r['likes']} comments={r['comments']} shares={r['shares']} saves={r['saves']} | theme={r['theme']} | {r['url']}")
    print('   ', r['content'][:100].replace('\n', ' '))

# --- per-account medians (IG reels vs statics, TT) ---
print('\n=== medians by account/type (views) ===')
groups = {}
for r in rows:
    acc = r['account']
    kind = acc.split('_')[1] + ('_reel' if r['is_reel'] == 'True' else '_static')
    v = num(r['views'])
    if v is not None:
        groups.setdefault((acc, kind), []).append(v)
for (acc, kind), vals in sorted(groups.items()):
    print(f"{acc:9s} {kind:10s} n={len(vals):3d} median={statistics.median(vals):8.0f}")

# --- yesterday (Oct 13) for context, most recent full day ---
print('\n=== Oct 13 (yesterday) summary ===')
for r in rows:
    if r['date'] == '2026-10-13':
        print(f"{r['account']} | reel={r['is_reel']} | views={r['views']} | theme={r['theme']}")
