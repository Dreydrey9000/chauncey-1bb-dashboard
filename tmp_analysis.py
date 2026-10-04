import csv, statistics

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
print("columns:", list(rows[0].keys()))
recent = [r for r in rows if r['date'] >= '2026-09-28']
print(f"--- posts since 2026-09-28 ({len(recent)}) ---")
for r in sorted(recent, key=lambda r: (r['date'], r['account'])):
    print(r['account'], r['date'], 'views=', r['views'], 'comments=', r['comments'],
          'likes=', r['likes'], 'saves=', r['saves'], 'reel=', r['is_reel'],
          'theme=', r['theme'], '|', (r['content'] or '')[:60].replace('\n', ' '))
print()
for acct in sorted(set(r['account'] for r in rows)):
    sub = [r for r in rows if r['account'] == acct]
    v = [int(r['views']) for r in sub if r['views']]
    last = max(r['date'] for r in sub)
    if v:
        print(f"{acct}: n={len(v)} median_views={statistics.median(v):.0f} max={max(v)} last_post={last}")
