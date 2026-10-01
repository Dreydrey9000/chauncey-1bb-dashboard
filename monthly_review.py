#!/usr/bin/env python3
"""Monthly pattern review — 30/60/90 medians + significance + content-class analysis.
Reads posts_all.csv (rebuilt from OFFICIAL_API Zernio pulls same run)."""
import csv, statistics, math, datetime

PATH = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv'
TODAY = datetime.date(2026, 10, 1)
rows = []
for r in csv.DictReader(open(PATH, newline='', encoding='utf-8')):
    r['date_dt'] = datetime.date.fromisoformat(r['date'])
    for k in ('views', 'reach', 'likes', 'comments', 'shares', 'saves'):
        r[k] = int(r[k] or 0)
    r['er_f'] = float(r['er']) if r['er'] not in ('', None) else None
    r['reel'] = r['is_reel'] == 'True'
    rows.append(r)

def med(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None

def mann_whitney(a, b):
    """Two-sided Mann-Whitney U exact-ish via normal approx; returns (U, z, p)."""
    n1, n2 = len(a), len(b)
    if n1 < 3 or n2 < 3:
        return None
    allv = sorted([(v, 1) for v in a] + [(v, 2) for v in b])
    # rank with ties
    ranks = {}
    i = 0
    ranked = []
    while i < len(allv):
        j = i
        while j < len(allv) and allv[j][0] == allv[i][0]:
            j += 1
        avg = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranked.append((allv[k][1], avg))
        i = j
    r1 = sum(rk for g, rk in ranked if g == 1)
    U1 = r1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    # tie correction
    from collections import Counter
    tie_counts = Counter(v for v, _ in allv)
    tie_term = sum(t**3 - t for t in tie_counts.values())
    N = n1 + n2
    sd = math.sqrt(n1 * n2 / 12 * ((N + 1) - tie_term / (N * (N - 1))))
    if sd == 0:
        return None
    z = (U1 - mu) / sd
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return U1, z, p

def q(vals, p):
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return None
    idx = p * (len(vals) - 1)
    lo, hi = int(math.floor(idx)), int(math.ceil(idx))
    return vals[lo] + (vals[hi] - vals[lo]) * (idx - lo)

ACCOUNTS = ['drey_ig', 'kevin_ig', 'drey_tt', 'kevin_tt', 'club_ig']
print(f'=== posts_all.csv: {len(rows)} rows, {min(r["date"] for r in rows)} -> {max(r["date"] for r in rows)} ===')

for acct in ACCOUNTS:
    d = [r for r in rows if r['account'] == acct]
    if not d:
        print(f'\n--- {acct}: NO POSTS in window ---')
        continue
    print(f'\n--- {acct} (n={len(d)}) ---')
    print(f'{"window":<8}{"n":>4}{"medViews":>10}{"p25":>8}{"p75":>8}{"medER%":>8}{"medSaves":>9}{"medComm":>8}{"medLikes":>9}{"medReach":>10}')
    for label, days in (('30d', 30), ('60d', 60), ('90d', 90)):
        cut = TODAY - datetime.timedelta(days=days)
        w = [r for r in d if r['date_dt'] > cut]
        if not w:
            print(f'{label:<8}{0:>4}  (no posts)')
            continue
        print(f'{label:<8}{len(w):>4}{med([r["views"] for r in w]):>10.0f}'
              f'{q([r["views"] for r in w], .25):>8.0f}{q([r["views"] for r in w], .75):>8.0f}'
              f'{(med([r["er_f"] for r in w]) or 0):>8.1f}'
              f'{med([r["saves"] for r in w]):>9.0f}{med([r["comments"] for r in w]):>8.0f}'
              f'{med([r["likes"] for r in w]):>9.0f}{med([r["reach"] for r in w]):>10.0f}')
    # significance: 30d vs 31-60d, and 31-60 vs 61-90, on views
    c30 = TODAY - datetime.timedelta(days=30)
    c60 = TODAY - datetime.timedelta(days=60)
    r30 = [r['views'] for r in d if r['date_dt'] > c30]
    r3160 = [r['views'] for r in d if c60 < r['date_dt'] <= c30]
    r6190 = [r['views'] for r in d if r['date_dt'] <= c60]
    for name, a, b in (('30d vs 31-60d', r30, r3160), ('31-60d vs 61-90d', r3160, r6190)):
        mw = mann_whitney(a, b)
        if mw:
            U, z, p = mw
            flag = ' *** REAL TREND' if p < 0.05 else ' (not significant)'
            print(f'  views {name}: med {med(a):.0f} vs {med(b):.0f}  z={z:+.2f} p={p:.3f}{flag}')
        else:
            print(f'  views {name}: n too small ({len(a)} vs {len(b)}) — cannot test')

# ---- content class: top/bottom 10 per IG account ----
for acct in ('drey_ig', 'kevin_ig'):
    d = [r for r in rows if r['account'] == acct]
    if not d:
        print(f'\n=== {acct}: no posts — cannot rank ===')
        continue
    print(f'\n=== {acct} TOP 10 by views ===')
    for r in sorted(d, key=lambda r: -r['views'])[:10]:
        snippet = ' '.join((r['content'] or '').split())[:95]
        print(f'  {r["date"]} {r["views"]:>7,}v er={r["er"] or "?"}\u0025 s={r["saves"]:>3} c={r["comments"]:>3} '
              f'{"REEL" if r["reel"] else "STAT"} [{r["theme"]}] {snippet}')
    print(f'=== {acct} BOTTOM 10 by views ===')
    for r in sorted(d, key=lambda r: r['views'])[:10]:
        snippet = ' '.join((r['content'] or '').split())[:95]
        print(f'  {r["date"]} {r["views"]:>7,}v er={r["er"] or "?"}\u0025 s={r["saves"]:>3} c={r["comments"]:>3} '
              f'{"REEL" if r["reel"] else "STAT"} [{r["theme"]}] {snippet}')
    # theme + format aggregates over full window
    print(f'=== {acct} theme aggregates (90d window) ===')
    groups = {}
    for r in d:
        groups.setdefault(r['theme'], []).append(r)
    for th, g in sorted(groups.items(), key=lambda kv: -(med([r['views'] for r in kv[1]]) or 0)):
        print(f'  [{th:<12}] n={len(g):>3}  medV={med([r["views"] for r in g]):>7.0f}  '
              f'medER={med([r["er_f"] for r in g]) or 0:>5.1f}  totSaves={sum(r["saves"] for r in g):>4}  '
              f'totComm={sum(r["comments"] for r in g):>3}')
    reels = [r for r in d if r['reel']]
    stats_ = [r for r in d if not r['reel']]
    if reels and stats_:
        print(f'  format: REEL n={len(reels)} medV={med([r["views"] for r in reels]):.0f} | '
              f'STATIC n={len(stats_)} medV={med([r["views"] for r in stats_]):.0f}')

# last-14d cadence check per account (for mix-hypothesis grading)
print('\n=== cadence: posts in last 14 / 30 days per account ===')
for acct in ACCOUNTS:
    d = [r for r in rows if r['account'] == acct]
    n14 = len([r for r in d if r['date_dt'] > TODAY - datetime.timedelta(days=14)])
    n30 = len([r for r in d if r['date_dt'] > TODAY - datetime.timedelta(days=30)])
    print(f'  {acct:<10} 14d={n14:>2}  30d={n30:>2}')
