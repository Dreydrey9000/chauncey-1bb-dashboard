import json, os
r = json.load(open(os.path.expanduser('~/.hermes/workspaces/chauncey/briefs/work/mb_2026-11-20.json')))
for key in ['drey_ig', 'kevin_ig']:
    acc = r['accounts'][key]
    print(f"===== {key} ({acc['handle']}) =====")
    print('YDAY:', json.dumps({k: v for k, v in acc['yesterday'].items() if k != 'posts_today'}))
    for p in acc['yesterday']['posts_today']:
        print('  -', p['type'], '| imp', p['impressions'], '| reach', p['reach'], '| L', p['likes'], 'C', p['comments'], 'Sh', p['shares'], 'Sv', p['saves'], '| skip', p['skipRate'], '|', p['caption'][:60])
    print('W1:', json.dumps(acc['w1']))
    print('W2:', json.dumps(acc['w2']))
    print('FOLLOWERS:', json.dumps(acc['followers']))
    print('TOP POSTS THIS WEEK:')
    for t in acc['top_posts']:
        print('  -', t['date'], t['type'], '| imp', t['impressions'], '| reach', t['reach'], '| L', t['likes'], 'C', t['comments'], 'Sh', t['shares'], 'Sv', t['saves'], '| skip', t['skipRate'], '| watch_ms', t['avgWatchMs'])
        print('    "', t['caption'][:110], '"')
    print('DAILY (14d):')
    for d, v in acc['daily'].items():
        print(f"  {d}: posts={v['posts']} (r{v['reels']}/s{v['stories']}/f{v['feed']}) reach={v['reach']} imp={v['impressions']} L{v['likes']} C{v['comments']} Sh{v['shares']} Sv{v['saves']} pv={v['profileViews']} wc={v['websiteClicks']}")
