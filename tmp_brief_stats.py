# Morning brief analysis: founder medians + last posts from posts_all.csv
import csv, statistics
from collections import defaultdict

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = []
with open(path, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def iv(r, k):
    v = (r.get(k) or "").strip()
    try:
        return float(v)
    except:
        return None

for r in rows:
    r['d'] = r['date']
    r['v'] = iv(r, 'views')

dates = sorted(r['d'] for r in rows if r['d'])
print("CSV date range:", dates[0], "->", dates[-1], "| total rows:", len(rows))

# last 14 days medians per account x format
cutoff = "2026-10-24"
def med(vals):
    vals = sorted(vals)
    return statistics.median(vals) if vals else None

for a in ['drey_ig', 'kevin_ig']:
    win = [r for r in rows if r['account'] == a and r['d'] >= cutoff]
    reels = [r['v'] for r in win if r['is_reel'] == 'True' and r['v']]
    stats_ = [r['v'] for r in win if r['is_reel'] != 'True' and r['v']]
    print(f"\n{a} 14d window ({cutoff}+): n={len(win)} | reels n={len(reels)} median={med(reels)} | statics n={len(stats_)} median={med(stats_)}")

print("\n== Last 10 posts per IG account (newest last) ==")
for a in ['drey_ig', 'kevin_ig']:
    sub = sorted([r for r in rows if r['account'] == a and r['d']], key=lambda r: r['d'])[-10:]
    print(f"\n--- {a} ---")
    for r in sub:
        print(f"{r['d']} v={r['v'] or 0:>6.0f} c={r['comments'] or 0:>3} likes={r['likes'] or 0:>4} reel={r['is_reel']:5s} theme={r['theme']:12s} | {r['content'][:80].replace(chr(10), ' ')}")

# theme medians 14d
print("\n== 14d theme medians ==")
agg = defaultdict(list)
for r in rows:
    if r['d'] >= cutoff and r['account'] in ('drey_ig', 'kevin_ig') and r['v']:
        agg[(r['account'], r['theme'])].append(r['v'])
for k in sorted(agg):
    vs = agg[k]
    if len(vs) >= 2:
        print(f"{k[0]} {k[1]:14s} n={len(vs)} median={med(vs):.0f}")

# comment counts on drey ranking reels specifically
print("\n== Drey IG reels w/ comments detail (14d) ==")
for r in sorted([r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and r['d'] >= cutoff], key=lambda r: r['d']):
    if r['v']:
        print(f"{r['d']} views={r['v']:.0f} comments={r['comments']} likes={r['likes']} shares={r['shares']} saves={r['saves']} | {r['content'][:70].replace(chr(10),' ')}")

print("\n== Kevin IG posts detail (14d) ==")
for r in sorted([r for r in rows if r['account'] == 'kevin_ig' and r['d'] >= cutoff], key=lambda r: r['d']):
    if r['v']:
        try:
            wm = float(r['watch_ms'] or 0); dur = float(r['dur_s'] or 0) if (r['dur_s'] or '').strip() else 0
            comp = f"{(wm/1000)/dur*100:.0f}%" if wm and dur else "-"
        except:
            comp = "-"
        print(f"{r['d']} v={r['v']:.0f} c={r['comments']} likes={r['likes']} reel={r['is_reel']} comp={comp} | {r['content'][:70].replace(chr(10),' ')}")
