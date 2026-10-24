# Morning-brief CSV grounding: recent posts + per-account medians
import csv, statistics, datetime

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = []
with open(path, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

print("total rows:", len(rows))
accounts = {}
for r in rows:
    accounts.setdefault(r['account'], 0)
    accounts[r['account']] += 1
print("accounts:", accounts)

def v(x):
    try:
        return float(x) if x not in ('', None, 'nan') else None
    except Exception:
        return None

def is_reel(r):
    return r.get('is_reel') in ('True', 'true', '1')

for acc in sorted(accounts):
    vals = [v(r['views']) for r in rows if r['account'] == acc and is_reel(r)]
    vals = [x for x in vals if x is not None]
    if vals:
        print(acc, "reels n=", len(vals), "median views=", statistics.median(vals))

dates = sorted(r['date'] for r in rows if r['date'])
print("date range:", dates[0], "->", dates[-1])

cutoff = (datetime.date(2026, 10, 24) - datetime.timedelta(days=14)).isoformat()
recent = [r for r in rows if r['date'] >= cutoff]
print("recent 14d posts:", len(recent))
for r in sorted(recent, key=lambda r: r['ts'], reverse=True)[:24]:
    print(r['date'], r['account'], "reel" if is_reel(r) else "static",
          "views=", r['views'], "likes=", r['likes'], "comments=", r['comments'],
          "theme=", (r['theme'] or '')[:24], "|", (r['content'] or '').replace("\n", " ")[:60])

# theme medians for the two founders (reels+static, by views)
for acc in ("drey_ig", "kevin_ig"):
    themes = {}
    for r in rows:
        if r['account'] == acc and r['theme']:
            themes.setdefault(r['theme'], []).append(v(r['views']))
    print("--- themes", acc)
    for t, vals in sorted(themes.items(), key=lambda kv: -statistics.median([x for x in kv[1] if x is not None] or [0])):
        vv = [x for x in vals if x is not None]
        if vv:
            print(f"  {t}: n={len(vv)} median={statistics.median(vv):.0f} max={max(vv):.0f}")
