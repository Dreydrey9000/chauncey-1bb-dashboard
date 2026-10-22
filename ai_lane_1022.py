# ai lane median for Drey (theme key = ai_systems in posts_all.csv)
import csv, statistics
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
v = [int(r['views']) for r in rows if r['account']=='drey_ig' and r['is_reel']=='True' and r['theme'] in ('ai_systems','ai-tool') and r['views'].isdigit()]
print('Drey IG AI-lane reels:', (statistics.median(v), len(v)) if v else (None, 0))
# kevin themes sanity: identity vs room statics
for th in ('identity','room','faith','family'):
    vv = [int(r['views']) for r in rows if r['account']=='kevin_ig' and r['is_reel']!='True' and r['theme']==th and r['views'].isdigit()]
    if vv: print('Kevin statics', th, (statistics.median(vv), len(vv)))
