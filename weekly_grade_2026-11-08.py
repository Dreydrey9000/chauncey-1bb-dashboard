# Weekly grading + WoW medians for 2026-11-08 review
import pandas as pd
import json

df = pd.read_csv('posts_all.csv', parse_dates=['ts'])
pd.set_option('display.width', 250)

ACCOUNTS = ['drey_ig', 'kevin_ig', 'drey_tt', 'kevin_tt', 'club_ig']
NUM = ['views', 'reach', 'likes', 'comments', 'shares', 'saves', 'er', 'dur_s']
for c in NUM:
    df[c] = pd.to_numeric(df[c], errors='coerce')


def med(s):
    s = s.dropna()
    if len(s) == 0:
        return 'unavail', 0
    return round(float(s.median()), 2), len(s)


def week_stats(acc, a, b, label):
    m = df[(df.account == acc) & (df.date >= a) & (df.date <= b)]
    out = [f'{acc} {label} ({a}..{b}): n={len(m)}']
    for c in ['views', 'er', 'saves', 'comments']:
        v, n = med(m[c])
        out.append(f'  {c}: median={v} (n_avail={n})')
    return '\n'.join(out)


print('=== A. WEEK OVER WEEK MEDIANS ===')
for acc in ACCOUNTS:
    print(week_stats(acc, '2026-10-26', '2026-11-01', 'W-prior'))
    print(week_stats(acc, '2026-11-02', '2026-11-08', 'W-this'))
    print()

print('=== B. LINE 31 drey_ig 2026-10-01 final (due Oct 29): 30d median thru Oct 29 + weekly compliance ===')
w30 = df[(df.account == 'drey_ig') & (df.date >= '2026-09-30') & (df.date <= '2026-10-29')]
v, n = med(w30.views)
print(f'drey_ig 30d thru Oct29: n={len(w30)} median views={v} (n_avail={n})')
for a, b in [('2026-10-05', '2026-10-11'), ('2026-10-12', '2026-10-18'),
             ('2026-10-19', '2026-10-25'), ('2026-10-26', '2026-10-29')]:
    m = df[(df.account == 'drey_ig') & (df.date >= a) & (df.date <= b)]
    reels = m[m.is_reel == True] if 'is_reel' in m else m[m.dur_s.notna()]
    print(f'  {a}..{b}: n={len(m)} (reels={len(reels)})')

print()
print('=== C. LINE 32 kevin_ig 2026-10-01 final (due Oct 29): 30d median thru Oct 29 ===')
w30k = df[(df.account == 'kevin_ig') & (df.date >= '2026-09-30') & (df.date <= '2026-10-29')]
v, n = med(w30k.views)
print(f'kevin_ig 30d thru Oct29: n={len(w30k)} median views={v} (n_avail={n})')

print()
print('=== D. LINE 33 drey_tt final (end Oct): October median ===')
oct_dt = df[(df.account == 'drey_tt') & (df.date >= '2026-10-01') & (df.date <= '2026-10-31')]
v, n = med(oct_dt.views)
print(f'drey_tt October: n={len(oct_dt)} median views={v} (n_avail={n})')

print()
print('=== E. LINE 34/50 club_ig: all posts + followers ===')
cp = df[df.account == 'club_ig']
for _, r in cp.iterrows():
    print(f'  {r.date} | views={r.views} likes={r.likes} comments={r.comments} saves={r.saves} er={r.er} | {str(r.content)[:80]}')
try:
    fj = json.load(open('raw/followers.json'))
    print('followers.json:', json.dumps(fj)[:400])
except Exception as e:
    print('followers.json read error:', e)

print()
print('=== F. LINE 47 drey_ig Oct 26 - Nov 1: every post (classify confession lane) ===')
m = df[(df.account == 'drey_ig') & (df.date >= '2026-10-26') & (df.date <= '2026-11-01')].sort_values('date')
for _, r in m.iterrows():
    print(f'  {r.date} | reel={r.is_reel} dur={r.dur_s} | v={r.views} l={r.likes} c={r.comments} s={r.saves} er={r.er} | {str(r.content)[:95]}')

print()
print('=== G. LINE 48 kevin_ig Oct 26 - Nov 1: every post w/ saves ===')
m = df[(df.account == 'kevin_ig') & (df.date >= '2026-10-26') & (df.date <= '2026-11-01')].sort_values('date')
for _, r in m.iterrows():
    print(f'  {r.date} | reel={r.is_reel} dur={r.dur_s} | v={r.views} s={r.saves} c={r.comments} er={r.er} | {str(r.content)[:95]}')

print()
print('=== H. LINE 49 kevin_tt Oct 26 - Nov 1: every post ===')
m = df[(df.account == 'kevin_tt') & (df.date >= '2026-10-26') & (df.date <= '2026-11-01')].sort_values('date')
for _, r in m.iterrows():
    print(f'  {r.date} | v={r.views} l={r.likes} c={r.comments} s={r.saves} er={r.er} | {str(r.content)[:95]}')

print()
print('=== I. THIS WEEK Nov 2-8: every post per founder account (for narrative + filming calls) ===')
for acc in ['drey_ig', 'kevin_ig', 'drey_tt', 'kevin_tt', 'club_ig']:
    m = df[(df.account == acc) & (df.date >= '2026-11-02') & (df.date <= '2026-11-08')].sort_values('date')
    print(f'--- {acc} (n={len(m)}) ---')
    for _, r in m.iterrows():
        print(f'  {r.date} | reel={r.is_reel} dur={r.dur_s} | v={r.views} l={r.likes} c={r.comments} s={r.saves} er={r.er} | {str(r.content)[:95]}')

print()
print('=== J. kevin_ig statics vs reels last 28d (thru Nov 8) for format context ===')
w28 = df[(df.account == 'kevin_ig') & (df.date >= '2026-10-11') & (df.date <= '2026-11-08')]
for lab, sub in [('statics', w28[w28.is_reel == False]), ('reels', w28[w28.is_reel == True])]:
    v, n = med(sub.views)
    sv, _ = med(sub.saves)
    print(f'  {lab}: n={len(sub)} medV={v} (avail={n}) medSaves={sv}')

print()
print('=== K. drey_ig confession-lane check Nov 2-8 (keyword scan) ===')
m = df[(df.account == 'drey_ig') & (df.date >= '2026-11-02') & (df.date <= '2026-11-08')]
kw = ['pound', 'i eat', 'i was', 'used to', 'struggl', 'confess', 'fail', 'hate', 'afraid', 'scared', 'embarrass']
for _, r in m.iterrows():
    cap = str(r.content).lower()
    hit = [k for k in kw if k in cap]
    print(f'  {r.date} | v={r.views} c={r.comments} er={r.er} | kw={hit} | {str(r.content)[:95]}')
