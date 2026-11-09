# Verify details before writing grades
import pandas as pd
df = pd.read_csv('posts_all.csv', parse_dates=['ts'])
for c in ['views', 'comments', 'saves', 'er']:
    df[c] = pd.to_numeric(df[c], errors='coerce')

print('--- drey_tt posts since Oct 20 ---')
m = df[(df.account == 'drey_tt') & (df.date >= '2026-10-20')]
for _, r in m.iterrows():
    print(f'  {r.date} | v={r.views} l={r.likes} c={r.comments} | {str(r.content)[:90]}')

print()
print('--- max comments per account, 90d window ---')
for acc in ['drey_ig', 'kevin_ig', 'kevin_tt', 'drey_tt']:
    sub = df[df.account == acc].nlargest(3, 'comments')
    for _, r in sub.iterrows():
        print(f'  {acc} {r.date} | c={r.comments} v={r.views} | {str(r.content)[:60]}')

print()
print('--- drey_ig utility subset median Nov 2-8 (7 second-person pain->tool reels) ---')
print('computed by hand: [102,208,224,271,271,328,722] median =', pd.Series([102,208,224,271,271,328,722]).median())
print('tier-lists: [121,169,1745] median =', pd.Series([121,169,1745]).median())

print()
print('--- 30d medians thru Nov 8 (context) ---')
for acc in ['drey_ig', 'kevin_ig', 'kevin_tt', 'drey_tt']:
    w = df[(df.account == acc) & (df.date >= '2026-10-09') & (df.date <= '2026-11-08')]
    print(f'  {acc}: n={len(w)} 30d median views={w.views.median()}')

print()
print('--- kevin_ig comments sum Nov 2-8 vs Oct 26-Nov 1 ---')
a = df[(df.account == 'kevin_ig') & (df.date >= '2026-11-02') & (df.date <= '2026-11-08')].comments.sum()
b = df[(df.account == 'kevin_ig') & (df.date >= '2026-10-26') & (df.date <= '2026-11-01')].comments.sum()
print(f'  this week sum={a} | prior week sum={b}')
