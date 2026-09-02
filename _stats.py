import csv, statistics
from collections import defaultdict
rows = list(csv.DictReader(open('posts_all.csv')))
by = defaultdict(list)
for r in rows:
    by[r['account']].append(r)
for acct, rs in by.items():
    rs.sort(key=lambda r: r['ts'])
    views = [int(r['views']) for r in rs if r['views']]
    print("== %s: n=%d latest=%s median=%s" % (acct, len(rs), rs[-1]['date'], int(statistics.median(views)) if views else 'NA'))
    for r in rs[-3:]:
        print("  %s v=%s c=%s reel=%s theme=%s | %s" % (r['date'], r['views'], r['comments'], r['is_reel'], r['theme'], r['content'][:60].replace('\n', ' ')))
for acct in ['drey_ig', 'kevin_ig']:
    th = defaultdict(list)
    for r in by[acct]:
        if r['views']:
            th[r['theme']].append(int(r['views']))
    print("\n%s theme medians:" % acct)
    for t, vs in sorted(th.items(), key=lambda x: -statistics.median(x[1])):
        print("  %s: median=%d n=%d" % (t, int(statistics.median(vs)), len(vs)))
