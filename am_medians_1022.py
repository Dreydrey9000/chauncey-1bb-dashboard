# AM brief 2026-10-22: medians from fresh posts_all.csv + latest founder posts
import csv, statistics
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
def med(f):
    v = [int(r['views']) for r in rows if f(r) and r['views'].isdigit()]
    return (statistics.median(v), len(v)) if v else (None, 0)
print('max date in CSV:', max(r['date'] for r in rows))
print('Drey IG reels all:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True'))
print('Drey IG confession:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True' and r['theme']=='confession'))
print('Drey IG room:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True' and r['theme']=='room'))
print('Drey IG ai-tool:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True' and r['theme']=='ai-tool'))
print('Drey IG statics:', med(lambda r: r['account']=='drey_ig' and r['is_reel']!='True'))
print('Kevin IG statics:', med(lambda r: r['account']=='kevin_ig' and r['is_reel']!='True'))
print('Kevin IG reels:', med(lambda r: r['account']=='kevin_ig' and r['is_reel']=='True'))
print('Kevin IG identity statics:', med(lambda r: r['account']=='kevin_ig' and r['is_reel']!='True' and r['theme']=='identity'))
print()
print('--- posts since 2026-10-20 ---')
for r in rows:
    if r['date'] >= '2026-10-20':
        print(r['account'], r['date'], 'reel' if r['is_reel']=='True' else 'static', r['theme'], '| views', r['views'], '| likes', r['likes'], '| comments', r['comments'], '|', r['content'][:60].replace('\n',' '))
