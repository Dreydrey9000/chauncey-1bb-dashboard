#!/usr/bin/env python3
"""Weekly review 2026-10-04: grade ungraded predictions + week-over-week medians."""
import pandas as pd

df = pd.read_csv('posts_all.csv')
df['date'] = pd.to_datetime(df['date'])

W = '2026-09-28'  # this week start (Sun)
P = '2026-09-21'  # prior week start

def med(s):
    s = s.dropna()
    return round(s.median(), 1) if len(s) else None

print('=== WEEK-OVER-WEEK MEDIANS (views / ER% / saves / comments) ===')
for acct in ['drey_ig', 'kevin_ig', 'drey_tt', 'kevin_tt', 'club_ig']:
    for label, lo in [('THIS wk 9/28-10/4', W), ('PRIOR wk 9/21-9/27', P)]:
        w = df[(df.account == acct) & (df.date >= lo) & (df.date < str(pd.Timestamp(lo) + pd.Timedelta(days=7))[:10])]
        v, e, s, c = med(w.views), med(w.er), med(w.saves), med(w.comments)
        print(f'{acct:9s} {label}: n={len(w):2d} views={v} ER={e} saves={s} comments={c}')
    print()

print('=== P1 drey_ig Sep28-Oct4: all posts (room-question reel? volume floor >=3?) ===')
w = df[(df.account == 'drey_ig') & (df.date >= W)].sort_values('date')
for _, r in w.iterrows():
    print(f'{r.date.date()} reel={r.is_reel} dur={r.dur_s}s v={r.views} c={r.comments} s={r.saves} likes={r.likes} er={r.er} theme={r.theme}')
    print(f'   {str(r.content)[:110]}')

print()
print('=== P2 kevin_ig Sep28-Oct4: reels w/ dur + engagement (confession-reel >=750v >=4s >=4ER? loops stopped?) ===')
w = df[(df.account == 'kevin_ig') & (df.date >= W)].sort_values('date')
for _, r in w.iterrows():
    print(f'{r.date.date()} reel={r.is_reel} dur={r.dur_s}s v={r.views} c={r.comments} s={r.saves} er={r.er} theme={r.theme}')
    print(f'   {str(r.content)[:110]}')

print()
print('=== P3 kevin_tt Sep28-Oct4: posts/day (cross-post cap?) + views ===')
w = df[(df.account == 'kevin_tt') & (df.date >= W)].sort_values('ts')
for _, r in w.iterrows():
    print(f'{r.date.date()} v={r.views} c={r.comments} s={r.saves} theme={r.theme}')
    print(f'   {str(r.content)[:100]}')
print('posts per day:')
print(w.groupby(w.date.dt.date).size().to_dict())

print()
print('=== P4/P5 interim: 30d medians (Sep 5-Oct 4) ===')
for acct in ['drey_ig', 'kevin_ig']:
    m = df[(df.account == acct) & (df.date >= '2026-09-05')]
    print(f'{acct} 30d n={len(m)} median views={med(m.views)}')

print()
print('=== P6 drey_tt October median ===')
m = df[(df.account == 'drey_tt') & (df.date >= '2026-10-01')]
print(f'oct n={len(m)} median views={med(m.views)}')
print('=== P6b drey_tt last 4 weeks trend ===')
for lo in ['2026-09-07','2026-09-14','2026-09-21','2026-09-28']:
    hi = str(pd.Timestamp(lo) + pd.Timedelta(days=7))[:10]
    w = df[(df.account=='drey_tt') & (df.date>=lo) & (df.date<hi)]
    print(f'wk {lo}: n={len(w)} med={med(w.views)}')

print()
print('=== P7 club_ig posts total ===')
print(len(df[df.account=='club_ig']))

print()
print('=== best posts this week per founder (for decisions) ===')
for acct in ['drey_ig','kevin_ig','kevin_tt','drey_tt']:
    w = df[(df.account==acct) & (df.date>=W)].sort_values('views', ascending=False)
    if len(w):
        r = w.iloc[0]
        print(f'{acct} TOP: {r.date.date()} v={r.views} er={r.er} theme={r.theme} :: {str(r.content)[:90]}')
