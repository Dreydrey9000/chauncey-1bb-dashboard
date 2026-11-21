#!/opt/homebrew/bin/python3
"""AM inspire brief 2026-11-21: read founder own-data (posts_all.csv) and print the
rows + medians needed for the brief. Read-only; prints only."""
import csv, statistics, datetime, json

CSV = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv'
rows = []
with open(CSV, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def dt(r):
    try:
        return datetime.datetime.fromisoformat(r['ts'])
    except Exception:
        try:
            return datetime.datetime.fromisoformat(r['date'])
        except Exception:
            return None

for acct in ('drey', 'kevin'):
    for plat, pf in [('IG', lambda r: 'instagram.com' in r['url']), ('TT', lambda r: 'tiktok.com' in r['url'])]:
        sub = [r for r in rows if r['account'].lower().startswith(acct) and pf(r)]
        if not sub:
            continue
        sub.sort(key=lambda r: dt(r) or datetime.datetime.min, reverse=True)
        print(f"=== {acct} [{plat}]: {len(sub)} posts, 6 latest ===")
        for r in sub[:6]:
            print(f"{r['ts']} | reel={r['is_reel']} | theme={r['theme']} | views={r['views']} | likes={r['likes']} | comments={r['comments']} | {r['content'][:60]!r} | {r['url']}")
        for label, filt in [
            ('reels', lambda r: r['is_reel'].strip().lower() in ('1','true','yes')),
            ('statics', lambda r: r['is_reel'].strip().lower() not in ('1','true','yes')),
        ]:
            s = [num(r['views']) for r in sub if filt(r) and num(r['views']) is not None]
            if s:
                print(f"[{plat}] median views {label}: {statistics.median(s):.1f} (n={len(s)})")
        themes = {}
        for r in sub:
            t = (r['theme'] or '').strip()
            v = num(r['views'])
            if t and v is not None:
                themes.setdefault(t, []).append(v)
        for t, vs in sorted(themes.items(), key=lambda kv: -statistics.median([x for x in kv[1] if x is not None])):
            if len(vs) >= 2:
                print(f"[{plat}] theme {t}: median {statistics.median(vs):.1f} (n={len(vs)})")
        print()
