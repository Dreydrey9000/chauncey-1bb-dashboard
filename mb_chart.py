#!/usr/bin/env python3
"""Morning brief chart: 14-day reach vs impressions per founder, post-day markers."""
import json, datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BG, GOLD, DIM, TXT = '#0E1116', '#E3B458', '#E3B45855', '#C9CFD6'

def load(name):
    d = json.load(open(f'/tmp/mb_daily_{name}.json'))['dailyData']
    dates = [dt.date.fromisoformat(r['date']) for r in d]
    reach = [r['metrics'].get('reach') or 0 for r in d]
    impr = [r['metrics'].get('impressions') or 0 for r in d]
    posts = [r.get('postCount') or 0 for r in d]
    return dates, reach, impr, posts

fig, axes = plt.subplots(2, 1, figsize=(10, 7.2), facecolor=BG)
fig.suptitle('Founder Instagram — 14 Days (reach vs impressions)', color=GOLD, fontsize=14, fontweight='bold', y=0.97)

for ax, (name, label) in zip(axes, [('DREY', 'Drey @itisdrey'), ('KEVIN', 'Kevin @kclavier')]):
    dates, reach, impr, posts = load(name)
    ax.set_facecolor(BG)
    ax.plot(dates, impr, color=DIM, lw=1.8, label='Impressions', zorder=2)
    ax.plot(dates, reach, color=GOLD, lw=2.4, label='Reach', zorder=3)
    for x, n in zip(dates, posts):
        if n > 0:
            y = reach[dates.index(x)]
            ax.scatter([x], [y], s=60 + 60 * n, color='#FFFFFF', edgecolor=GOLD, lw=1.6, zorder=4)
            ax.annotate(str(n), (x, y), textcoords='offset points', xytext=(0, 9),
                        color=GOLD, fontsize=8, ha='center')
    ax.set_title(label, color=TXT, fontsize=11, loc='left')
    ax.tick_params(colors=TXT, labelsize=8)
    for s in ax.spines.values():
        s.set_color('#2A2F3A')
    ax.grid(color='#1C2129', lw=0.6)
    ax.legend(facecolor=BG, edgecolor='#2A2F3A', labelcolor=TXT, fontsize=8, loc='upper right')
    import matplotlib.dates as mdates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

fig.text(0.99, 0.01, 'white dot = post day (size/count)', color='#6B7280', fontsize=7, ha='right')
plt.tight_layout(rect=[0, 0.02, 1, 0.95])

day = dt.date.today().isoformat()
for path in (f'/Users/andrethomas/.hermes/workspaces/chauncey/briefs/morning_{day}.png',
             f'/Users/andrethomas/.hermes/workspaces/chauncey/site/assets/morning_{day}.png'):
    plt.savefig(path, dpi=150, facecolor=BG)
    print('saved', path)
