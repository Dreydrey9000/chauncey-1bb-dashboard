# Day-over-day mover check — compares today's raw/followers.json vs git HEAD~1's version
import json, subprocess

new = json.load(open('raw/followers.json'))

def series(obj):
    out = {}
    for a in obj['accounts']:
        pts = obj['stats'].get(a['_id'], [])
        if pts:
            out[a['username']] = (pts[-2]['followers'], pts[-1]['followers'], pts[-1]['date'])
    return out

cur = series(new)
old_raw = subprocess.run(['git', 'show', 'HEAD~1:raw/followers.json'], capture_output=True, text=True).stdout
old = series(json.loads(old_raw)) if old_raw.strip() else {}

print('latest points (username: prev -> last, date):')
for u, v in cur.items():
    print(f'  {u}: {v[0]} -> {v[1]} on {v[2]} (delta {v[1]-v[0]:+d})')
print('snapshot currentFollowers:', {a['username']: a['currentFollowers'] for a in new['accounts']})
print('vs HEAD~1 snapshot:', {a['username']: a['currentFollowers'] for a in json.loads(old_raw)['accounts']} if old_raw.strip() else 'n/a')
