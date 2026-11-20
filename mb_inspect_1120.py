import json, ast, os
d = json.load(open(os.path.expanduser('~/.hermes/workspaces/chauncey/dashboard/raw/drey_ig_p1.txt')))
pg = ast.literal_eval(d['result'])
print('overview:', json.dumps(pg.get('overview', {}))[:500])
posts = pg['posts']
print('n:', len(posts))
p = posts[0]
for k in sorted(p.keys()):
    print(k, '=', str(p[k])[:70])
print('---- analytics full keys, first post ----')
print(json.dumps(p.get('analytics'), indent=1)[:800])
print('---- mediaProductType values across pages ----')
import glob, collections
c = collections.Counter()
caps = 0
for f in sorted(glob.glob(os.path.expanduser('~/.hermes/workspaces/chauncey/dashboard/raw/drey_ig_p*.txt'))):
    pg2 = ast.literal_eval(json.load(open(f))['result'])
    for q in pg2['posts']:
        c[q.get('mediaProductType')] += 1
        if q.get('content'): caps += 1
print(c, 'with content:', caps)
q2 = [q for f in sorted(glob.glob(os.path.expanduser('~/.hermes/workspaces/chauncey/dashboard/raw/drey_ig_p*.txt'))) for q in ast.literal_eval(json.load(open(f))['result'])['posts'] if q.get('mediaProductType') != 'STORY']
if q2:
    z = q2[0]
    print('sample non-story:', z.get('mediaProductType'), z.get('publishedAt'), (z.get('content') or '')[:60], json.dumps(z.get('analytics'))[:300])
