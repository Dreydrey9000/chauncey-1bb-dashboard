# Morning brief founder stats — 2026-11-11 AM (fixed schema)
import csv, statistics as st
from datetime import datetime, timezone, timedelta

ET = timezone(timedelta(hours=-5))
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

# inspect account values
accts = {}
for r in rows:
    accts[r['account']] = accts.get(r['account'], 0) + 1
print('accounts:', accts)

def parse_ts(s):
    s = (s or '').strip()
    try:
        return datetime.fromisoformat(s)
    except Exception:
        pass
    return None

def num(s):
    try:
        return int(float(s))
    except Exception:
        return None

now = datetime(2026, 11, 11, 12, 0, tzinfo=timezone.utc)  # ~7a ET
for who in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == who]
    print('\n====', who, 'rows:', len(sub))
    dated = []
    for r in sub:
        ts = parse_ts(r.get('ts') or r.get('date') or '')
        dated.append((ts, r))
    dated.sort(key=lambda t: t[0] or datetime(1970, 1, 1, tzinfo=timezone.utc), reverse=True)
    for ts, r in dated[:12]:
        cap = (r.get('content') or '')[:80].replace('\n', ' ')
        reel = r.get('is_reel')
        print(f"  {ts} | reel={reel} theme={r.get('theme','')[:12]:12s} | v={num(r['views'])} c={num(r['comments'])} l={num(r['likes'])} | {cap}")
    cut = now - timedelta(days=30)
    def med(key, pred):
        vals = [num(r[key]) for ts, r in dated if pred(ts, r) and num(r[key]) is not None]
        return (st.median(vals), len(vals)) if vals else (None, 0)
    # medians: reels vs statics, and by theme
    mv, nv = med('views', lambda ts, r: ts and ts >= cut and r.get('is_reel') in ('True', 'true', '1', True))
    print(f"  30d REELS: views median={mv} (n={nv})")
    sv, ns = med('views', lambda ts, r: ts and ts >= cut and r.get('is_reel') not in ('True', 'true', '1', True))
    print(f"  30d STATICS: views median={sv} (n={ns})")
    themes = {}
    for ts, r in dated:
        if ts and ts >= cut:
            themes.setdefault(r.get('theme') or '?', []).append(r)
    for th, rs in sorted(themes.items(), key=lambda kv: -len(kv[1])):
        vv = [num(r['views']) for r in rs if num(r['views']) is not None]
        cc = [num(r['comments']) for r in rs if num(r['comments']) is not None]
        if vv:
            print(f"  30d theme={th}: n={len(rs)} views med={st.median(vv):.0f} comments med={st.median(cc) if cc else 0:.0f}")
    l24 = [(ts, r) for ts, r in dated if ts and ts >= now - timedelta(hours=36)]
    print(f"  last-36h posts: {len(l24)}")
    for ts, r in l24:
        print(f"    {ts} reel={r.get('is_reel')} v={num(r['views'])} c={num(r['comments'])} | {(r.get('content') or '')[:70]}")
