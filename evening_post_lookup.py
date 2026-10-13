#!/usr/bin/env python3
"""Print publishedAt + analytics for Kevin posts published 2026-10-09..10-13."""
import json, ast, glob

for fp in sorted(glob.glob('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/kevin_ig_p*.txt')):
    d = json.loads(open(fp).read())['result']
    p = ast.literal_eval(d) if isinstance(d, str) else d
    for post in p.get('posts') or []:
        pub = str(post.get('publishedAt') or '')
        if any(f'2026-10-{dd}' in pub for dd in ('09', '10', '11', '12', '13')):
            a = post.get('analytics') or {}
            cap = (post.get('content') or '')[:55].replace('\n', ' ')
            print(pub[:16], '| type', post.get('mediaType'), '| views', a.get('views'), 'likes', a.get('likes'),
                  'comments', a.get('comments'), 'saves', a.get('saves'), '|', cap)
