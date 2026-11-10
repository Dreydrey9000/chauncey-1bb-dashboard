#!/opt/homebrew/bin/python3
"""Morning inspire brief 2026-11-10: founder stats from posts_all.csv."""
import pandas as pd

df = pd.read_csv('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')
df['ts'] = pd.to_datetime(df['ts'])
df['date'] = pd.to_datetime(df['date'])

print("MAX DATE:", df['date'].max().date(), "| rows:", len(df))

# --- Drey IG: the 8am confession reel prediction from last night ---
print("\n=== DREY IG reels: last 8 ===")
drey_reels = df[(df['account'] == 'drey_ig') & (df['is_reel'] == True)].sort_values('ts').tail(8)
for _, r in drey_reels.iterrows():
    print(f"{r['date'].date()} {str(r['ts'])[:16]} views={r['views']:.0f} likes={r['likes']:.0f} cmts={r['comments']:.0f} theme={r['theme']} | {str(r['content'])[:60]}")

print("\n=== DREY IG: last 6 posts any type ===")
for _, r in df[df['account'] == 'drey_ig'].sort_values('ts').tail(6).iterrows():
    print(f"{r['date'].date()} {str(r['ts'])[:16]} views={r['views']:.0f} cmts={r['comments']:.0f} reel={r['is_reel']} theme={r['theme']} | {str(r['content'])[:60]}")

# Drey medians
d30 = df[(df['account'] == 'drey_ig') & (df['date'] >= df['date'].max() - pd.Timedelta(days=30))]
print("\nDrey IG 30d by theme:")
print(d30.groupby('theme')['views'].agg(['count', 'median', 'max']).sort_values('median', ascending=False).to_string())
d_statics = d30[d30['is_reel'] == False]['views']
d_reels = d30[d30['is_reel'] == True]['views']
print(f"Drey statics median (30d): {d_statics.median():.1f} (n={len(d_statics)}) | reels median: {d_reels.median():.1f} (n={len(d_reels)})")

# --- Kevin IG: ceiling static graded at 7am ---
print("\n=== KEVIN IG: last 8 posts ===")
for _, r in df[df['account'] == 'kevin_ig'].sort_values('ts').tail(8).iterrows():
    print(f"{r['date'].date()} {str(r['ts'])[:16]} views={r['views']:.0f} likes={r['likes']:.0f} cmts={r['comments']:.0f} reel={r['is_reel']} theme={r['theme']} | {str(r['content'])[:60]}")

k30 = df[(df['account'] == 'kevin_ig') & (df['date'] >= df['date'].max() - pd.Timedelta(days=30))]
print("\nKevin IG 30d by theme:")
print(k30.groupby('theme')['views'].agg(['count', 'median', 'max']).sort_values('median', ascending=False).to_string())
k_statics = k30[k30['is_reel'] == False]['views']
k_reels = k30[k30['is_reel'] == True]['views']
print(f"Kevin statics median (30d): {k_statics.median():.1f} (n={len(k_statics)}) | reels median: {k_reels.median():.1f} (n={len(k_reels)})")
# Kevin engagement rate on statics
k_statics_er = k30[k30['is_reel'] == False]['er']
print(f"Kevin statics ER median (30d): {k_statics_er.median():.2f}%")
# Kevin reels completion/watch
k_reels_watch = k30[(k30['is_reel'] == True) & (k30['watch_ms'] > 0)]
print(f"Kevin reels watch_ms median: {k_reels_watch['watch_ms'].median():.0f}ms over n={len(k_reels_watch)}")
