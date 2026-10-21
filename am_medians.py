# AM brief 2026-10-21: recompute medians from fresh posts_all.csv (post-6:30a refresh)
import csv, statistics
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
def med(f):
    v = [int(r['views']) for r in rows if f(r) and r['views'].isdigit()]
    return (statistics.median(v), len(v)) if v else (None, 0)
print('Drey IG reels all:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True'))
print('Drey IG confession:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True' and r['theme']=='confession'))
print('Drey IG room:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True' and r['theme']=='room'))
print('Drey IG ai-tool:', med(lambda r: r['account']=='drey_ig' and r['is_reel']=='True' and r['theme']=='ai-tool'))
print('Kevin IG statics:', med(lambda r: r['account']=='kevin_ig' and r['is_reel']!='True'))
print('Kevin IG reels:', med(lambda r: r['account']=='kevin_ig' and r['is_reel']=='True'))
print('Kevin IG identity statics:', med(lambda r: r['account']=='kevin_ig' and r['is_reel']!='True' and r['theme']=='identity'))
# last 5 rows sanity: account, date, views, theme
for r in rows[-5:]:
    print(r['account'], r['date'], r['views'], r['theme'], r['url'][-16:])
