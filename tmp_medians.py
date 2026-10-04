import csv, statistics

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

def med(acct, theme=None, reel=None):
    v = [int(r['views']) for r in rows
         if r['account'] == acct and r['views']
         and (theme is None or r['theme'] == theme)
         and (reel is None or (r['is_reel'] == 'True') == reel)]
    return (len(v), statistics.median(v)) if v else (0, None)

k = 'kevin_ig'; d = 'drey_ig'
print('kevin_ig all:', med(k))
print('kevin_ig static (is_reel False):', med(k, reel=False))
print('kevin_ig reel:', med(k, reel=True))
for t in ('identity', 'room', 'confession', 'discipline', 'family'):
    print(f'kevin_ig {t}:', med(k, theme=t))
for t in ('confession', 'room', 'ai_systems'):
    print(f'drey_ig {t}:', med(d, theme=t))
# kevin 10/03 post vs medians
for r in rows:
    if r['account'] == k and r['date'] == '2026-10-03':
        print('kevin 10/03:', r['views'], 'views | vs all-median x', round(int(r['views'])/1442, 1), '| vs static-median x', round(int(r['views'])/1084, 1) if 1084 else '')
# any posts dated 2026-10-04?
print('posts dated 10/04:', [r['account'] for r in rows if r['date'] == '2026-10-04'])
