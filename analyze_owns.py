# Own-data quick stats for the inspire brief (posts_all.csv, OFFICIAL_API via Zernio)
import csv, statistics, datetime, sys

CSV = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv'
rows = []
with open(CSV, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        for k in ('views', 'likes', 'comments', 'shares', 'saves'):
            try:
                r[k] = int(r[k] or 0)
            except ValueError:
                r[k] = 0
        rows.append(r)

today = datetime.date(2026, 10, 6)

for acct in ('drey_ig', 'kevin_ig'):
    rs = [r for r in rows if r['account'] == acct]
    rs.sort(key=lambda r: r['ts'], reverse=True)
    print('=' * 15, acct, '=' * 15)
    print('latest 6:')
    for r in rs[:6]:
        print(f"  {r['date']} {('REEL' if r['is_reel'] == 'True' else 'STAT')} theme={r['theme']:<11} views={r['views']:<6} likes={r['likes']:<4} com={r['comments']:<3} {r['url']}")
    last_date = datetime.date.fromisoformat(rs[0]['date'])
    print('days since last post:', (today - last_date).days)
    # theme medians (all time, n>=8 for stability)
    themes = {}
    for r in rs:
        themes.setdefault(r['theme'], []).append(r['views'])
    print('theme medians:')
    for t, v in sorted(themes.items(), key=lambda kv: -statistics.median(kv[1])):
        if len(v) >= 8:
            print(f"  {t:<12} median={int(statistics.median(v)):<6} n={len(v)}")
    # format split
    for fmt, flag in (('static', 'False'), ('reel', 'True')):
        v = [int(r['views']) for r in rs if r['is_reel'] == flag]
        if v:
            print(f'{fmt}: median={int(statistics.median(v))} n={len(v)}')
    # last-14-day window medians by theme
    cut = (today - datetime.timedelta(days=14)).isoformat()
    win = [r for r in rs if r['date'] >= cut]
    print(f'last-14d posts: {len(win)}')
    wthemes = {}
    for r in win:
        wthemes.setdefault(r['theme'], []).append(r['views'])
    for t, v in sorted(wthemes.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f'  14d {t:<12} median={int(statistics.median(v)):<6} n={len(v)}')
