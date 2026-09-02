#!/usr/bin/env python3
import json
d = json.loads(open('site/data.js').read().split('=', 1)[1].strip().rstrip(';'))
print('PREV generated:', d.get('generated'))
for k in ['drey_ig', 'kevin_ig', 'drey_tt', 'kevin_tt']:
    a = d.get(k) or {}
    print('PREV', k, 'posts=', a.get('posts'), 'meanViews=', a.get('meanViews'), 'maxViews=', a.get('maxViews'))
print('PREV dreyFollowers:', d.get('dreyFollowers'))
kf = d.get('kevinFollowers') or []
print('PREV kevinFollowers tail:', kf[-3:] if kf else None)
print('PREV clubFollowers:', d.get('clubFollowers'))
