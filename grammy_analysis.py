import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import warnings
warnings.filterwarnings('ignore')

os.makedirs("charts", exist_ok=True)
print("loading all datasets")

df_winners    = pd.read_csv("Grammy_Awards_Winners_20260208_055452.csv",     encoding='utf-8-sig')
df_big4       = pd.read_csv("Grammy_Big_Four_Awards_20260208_055452.csv",    encoding='utf-8-sig')
df_artists    = pd.read_csv("Grammy_Top_Artists_20260208_055452.csv",        encoding='utf-8-sig')
df_decade     = pd.read_csv("Grammy_Winners_By_Decade_20260208_055452.csv",  encoding='utf-8-sig')

print(" MAIN WINNERS DATASET")
print(f"Total rows     : {len(df_winners)}")
print(f"Years covered  : {df_winners['Year'].min()} - {df_winners['Year'].max()}")
print(f"Unique artists : {df_winners['Artist'].nunique()}")
print(f"Unique categories: {df_winners['Category'].nunique()}")
print(f"\nColumn names:\n{df_winners.columns.tolist()}")
print(f"\nFirst 3 rows:\n{df_winners.head(3)}")

print("top artist dataset")
print(df_artists.to_string())

print("winners by decade")
print(df_decade.to_string())

print("missing values check")
print(df_winners.isnull().sum())


# Golden Grammy color palette
GOLD       = '#FFD700'
DARK_GOLD  = '#B8860B'
CREAM      = '#FFF8DC'
DARK_BG    = '#1a1a2e'
MID_BG     = '#16213e'
ACCENT     = '#e94560'
PURPLE     = '#7b2d8b'
TEAL       = '#00b4d8'

plt.rcParams['figure.facecolor']  = DARK_BG
plt.rcParams['axes.facecolor']    = MID_BG
plt.rcParams['text.color']        = CREAM
plt.rcParams['axes.labelcolor']   = CREAM
plt.rcParams['xtick.color']       = CREAM
plt.rcParams['ytick.color']       = CREAM
plt.rcParams['axes.spines.top']   = False
plt.rcParams['axes.spines.right'] = False

print("\n🎨 Creating visualizations...")


# CHART 1: Top 10 Most Decorated Artists

print("\n Chart 1: Top 10 Artists...")

top10 = df_artists.head(10)

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(MID_BG)

bars = ax.barh(top10['Artist'], top10['Total_Wins'],
               color=[GOLD, DARK_GOLD, GOLD, DARK_GOLD, GOLD,
                      DARK_GOLD, GOLD, DARK_GOLD, GOLD, DARK_GOLD],
               edgecolor=CREAM, linewidth=0.8, height=0.6)

# Add value labels
for bar, val in zip(bars, top10['Total_Wins']):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f'{val} wins', va='center', fontsize=11,
            color=GOLD, fontweight='bold')

ax.set_xlabel('Total Grammy Wins', fontsize=13, labelpad=10)
ax.set_title('🏆 Most Decorated Grammy Artists of All Time',
             fontsize=18, fontweight='bold', color=GOLD, pad=20)
ax.set_xlim(0, top10['Total_Wins'].max() + 1.5)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.2, color=CREAM)
ax.tick_params(axis='y', labelsize=11)

plt.tight_layout()
plt.savefig('charts/01_top_artists.png', dpi=300, bbox_inches='tight',
            facecolor=DARK_BG)
print(" Saved: charts/01_top_artists.png")
plt.close()


# CHART 2: Winners by Decade (Stacked Bar)

print("\n Chart 2: Winners by Decade...")

decade_pivot = df_decade.pivot_table(
    index='Decade', columns='Category',
    values='Total_Winners', fill_value=0
).reset_index()

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(MID_BG)

colors     = [GOLD, ACCENT, TEAL, PURPLE, DARK_GOLD]
categories = [c for c in decade_pivot.columns if c != 'Decade']
bottom     = [0] * len(decade_pivot)

for i, cat in enumerate(categories):
    vals = decade_pivot[cat].values
    ax.bar(decade_pivot['Decade'].astype(str), vals,
           bottom=bottom, label=cat,
           color=colors[i % len(colors)],
           edgecolor=DARK_BG, linewidth=1.5, width=0.6)
    bottom = [b + v for b, v in zip(bottom, vals)]

ax.set_xlabel('Decade', fontsize=13, labelpad=10)
ax.set_ylabel('Number of Winners', fontsize=13, labelpad=10)
ax.set_title(' Grammy Winners by Decade & Category',
             fontsize=18, fontweight='bold', color=GOLD, pad=20)
ax.legend(loc='upper left', facecolor=MID_BG, edgecolor=GOLD,
          labelcolor=CREAM, fontsize=10)
ax.grid(axis='y', alpha=0.2, color=CREAM)

plt.tight_layout()
plt.savefig('charts/02_winners_by_decade.png', dpi=300,
            bbox_inches='tight', facecolor=DARK_BG)
print(" Saved: charts/02_winners_by_decade.png")
plt.close()


# CHART 3: Big Four Awards Over Time (Line)

print("\n Chart 3: Big Four Over Time...")

big4_yearly = df_big4.groupby(['Year', 'Category']).size().reset_index(name='Count')

fig, ax = plt.subplots(figsize=(16, 7))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(MID_BG)

cat_colors = {
    'Album of the Year'  : GOLD,
    'Record of the Year' : ACCENT,
    'Song of the Year'   : TEAL,
    'Best New Artist'    : PURPLE
}

for cat, color in cat_colors.items():
    data = big4_yearly[big4_yearly['Category'] == cat]
    if len(data) > 0:
        ax.plot(data['Year'], data['Count'],
                color=color, linewidth=2.5,
                label=cat, marker='o', markersize=4)

ax.set_xlabel('Year', fontsize=13, labelpad=10)
ax.set_ylabel('Number of Winners', fontsize=13, labelpad=10)
ax.set_title(' Big Four Grammy Awards Across All Ceremonies',
             fontsize=18, fontweight='bold', color=GOLD, pad=20)
ax.legend(facecolor=MID_BG, edgecolor=GOLD,
          labelcolor=CREAM, fontsize=10)
ax.grid(alpha=0.2, color=CREAM)

plt.tight_layout()
plt.savefig('charts/03_big4_over_time.png', dpi=300,
            bbox_inches='tight', facecolor=DARK_BG)
print(" Saved: charts/03_big4_over_time.png")
plt.close()


# CHART 4: Era Distribution Pie Chart

print("\n Chart 4: Era Distribution...")

era_counts = df_winners['Era'].value_counts()

fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(DARK_BG)

era_colors  = [GOLD, ACCENT, TEAL, PURPLE, DARK_GOLD,
               '#ff6b6b', '#4ecdc4', '#45b7d1']
explode     = [0.05] * len(era_counts)

wedges, texts, autotexts = ax.pie(
    era_counts.values,
    labels=era_counts.index,
    autopct='%1.1f%%',
    colors=era_colors[:len(era_counts)],
    explode=explode,
    startangle=140,
    textprops={'color': CREAM, 'fontsize': 11},
    wedgeprops={'edgecolor': DARK_BG, 'linewidth': 2}
)

for autotext in autotexts:
    autotext.set_color(DARK_BG)
    autotext.set_fontweight('bold')

ax.set_title(' Grammy Wins Distribution by Era',
             fontsize=18, fontweight='bold', color=GOLD, pad=20)

plt.tight_layout()
plt.savefig('charts/04_era_distribution.png', dpi=300,
            bbox_inches='tight', facecolor=DARK_BG)
print(" Saved: charts/04_era_distribution.png")
plt.close()


# CHART 5: Artist Win Timeline (Scatter)

print("\n Chart 5: Artist Win Timeline...")

top_artists_list = df_artists.head(10)['Artist'].tolist()
timeline_data    = df_winners[df_winners['Artist'].isin(top_artists_list)]

fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(MID_BG)

scatter_colors = [GOLD, ACCENT, TEAL, PURPLE, DARK_GOLD,
                  '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#dda0dd']

for i, artist in enumerate(top_artists_list):
    artist_data = timeline_data[timeline_data['Artist'] == artist]
    ax.scatter(artist_data['Year'],
               [artist] * len(artist_data),
               color=scatter_colors[i], s=200,
               zorder=5, edgecolors=CREAM, linewidth=1)

ax.set_xlabel('Year', fontsize=13, labelpad=10)
ax.set_title(' Grammy Win Timeline — Top 10 Artists',
             fontsize=18, fontweight='bold', color=GOLD, pad=20)
ax.grid(axis='x', alpha=0.2, color=CREAM)
ax.set_xlim(df_winners['Year'].min() - 2, df_winners['Year'].max() + 2)
ax.tick_params(axis='y', labelsize=10)

plt.tight_layout()
plt.savefig('charts/05_artist_timeline.png', dpi=300,
            bbox_inches='tight', facecolor=DARK_BG)
print(" Saved: charts/05_artist_timeline.png")
plt.close()

print("\n All 5 charts created!")
