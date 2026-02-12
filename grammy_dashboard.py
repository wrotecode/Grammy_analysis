

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
import warnings
warnings.filterwarnings('ignore')


# LOAD DATA

df_winners = pd.read_csv("Grammy_Awards_Winners_20260208_055452.csv",    encoding='utf-8-sig')
df_artists = pd.read_csv("Grammy_Top_Artists_20260208_055452.csv",       encoding='utf-8-sig')
df_decade  = pd.read_csv("Grammy_Winners_By_Decade_20260208_055452.csv", encoding='utf-8-sig')
df_big4    = pd.read_csv("Grammy_Big_Four_Awards_20260208_055452.csv",   encoding='utf-8-sig')

# COLOR PALETTE

GOLD     = '#FFD700'
DARK_BG  = '#1a1a2e'
MID_BG   = '#16213e'
CARD_BG  = '#0f3460'
ACCENT   = '#e94560'
TEAL     = '#00b4d8'
PURPLE   = '#7b2d8b'
CREAM    = '#FFF8DC'


# PRE-COMPUTE DATA

top10         = df_artists.head(10)
era_counts    = df_winners['Era'].value_counts().reset_index()
era_counts.columns = ['Era', 'Count']
decade_pivot  = df_decade.pivot_table(
    index='Decade', columns='Category',
    values='Total_Winners', fill_value=0
).reset_index()
big4_yearly   = df_big4.groupby(
    ['Year', 'Category']
).size().reset_index(name='Count')


# BUILD FIGURES


# Figure 1: Top Artists Bar
fig_artists = px.bar(
    top10,
    x='Total_Wins', y='Artist',
    orientation='h',
    color='Total_Wins',
    color_continuous_scale=[[0, '#B8860B'], [0.5, GOLD], [1, CREAM]],
    text='Total_Wins',
    labels={'Total_Wins': 'Total Wins', 'Artist': ''},
    title=' Most Decorated Grammy Artists of All Time'
)
fig_artists.update_traces(
    textposition='outside',
    textfont=dict(color=GOLD, size=13)
)
fig_artists.update_layout(
    plot_bgcolor=MID_BG, paper_bgcolor=DARK_BG,
    font_color=CREAM, title_font_color=GOLD,
    title_font_size=16,
    yaxis=dict(autorange='reversed'),
    coloraxis_showscale=False,
    margin=dict(l=20, r=40, t=50, b=20)
)

# Figure 2: Decade Stacked Bar
fig_decade = go.Figure()
cat_colors = [GOLD, ACCENT, TEAL, PURPLE, '#B8860B']
categories = [c for c in decade_pivot.columns if c != 'Decade']
for i, cat in enumerate(categories):
    fig_decade.add_trace(go.Bar(
        x=decade_pivot['Decade'].astype(str),
        y=decade_pivot[cat],
        name=cat,
        marker_color=cat_colors[i % len(cat_colors)]
    ))
fig_decade.update_layout(
    barmode='stack',
    plot_bgcolor=MID_BG, paper_bgcolor=DARK_BG,
    font_color=CREAM,
    title=dict(text=' Grammy Winners by Decade',
               font=dict(color=GOLD, size=16)),
    legend=dict(bgcolor=CARD_BG, bordercolor=GOLD,
                borderwidth=1, font=dict(color=CREAM)),
    margin=dict(l=20, r=20, t=50, b=20)
)

# Figure 3: Big Four Line Chart
fig_big4 = px.line(
    big4_yearly,
    x='Year', y='Count',
    color='Category',
    markers=True,
    color_discrete_sequence=[GOLD, ACCENT, TEAL, PURPLE],
    title=' Big Four Awards Across All Ceremonies'
)
fig_big4.update_layout(
    plot_bgcolor=MID_BG, paper_bgcolor=DARK_BG,
    font_color=CREAM, title_font_color=GOLD,
    title_font_size=16,
    legend=dict(bgcolor=CARD_BG, bordercolor=GOLD,
                borderwidth=1, font=dict(color=CREAM)),
    margin=dict(l=20, r=20, t=50, b=20)
)
fig_big4.update_xaxes(gridcolor='rgba(255,255,255,0.1)')
fig_big4.update_yaxes(gridcolor='rgba(255,255,255,0.1)')

# Figure 4: Era Pie
fig_era = px.pie(
    era_counts,
    names='Era', values='Count',
    color_discrete_sequence=[GOLD, ACCENT, TEAL, PURPLE,
                              '#B8860B', '#ff6b6b', '#4ecdc4'],
    title=' Wins by Era',
    hole=0.4
)
fig_era.update_layout(
    plot_bgcolor=DARK_BG, paper_bgcolor=DARK_BG,
    font_color=CREAM, title_font_color=GOLD,
    title_font_size=16,
    legend=dict(bgcolor=CARD_BG, font=dict(color=CREAM)),
    margin=dict(l=20, r=20, t=50, b=20)
)


# SUMMARY STATS

total_winners    = len(df_winners)
total_artists    = df_winners['Artist'].nunique()
years_covered    = f"{df_winners['Year'].min()}–{df_winners['Year'].max()}"
top_artist_name  = df_artists.iloc[0]['Artist']
top_artist_wins  = df_artists.iloc[0]['Total_Wins']


# BUILD DASH APP

app = dash.Dash(__name__)

app.layout = html.Div(style={
    'backgroundColor': DARK_BG,
    'fontFamily': 'Georgia, serif',
    'minHeight': '100vh',
    'padding': '0'
}, children=[

    # ---- HEADER ----
    html.Div(style={
        'background': f'linear-gradient(135deg, {DARK_BG}, {CARD_BG})',
        'padding': '40px 30px 30px',
        'borderBottom': f'3px solid {GOLD}',
        'textAlign': 'center'
    }, children=[
        html.H1(' THE GRAMMY EFFECT',
                style={'color': GOLD, 'fontSize': '3rem',
                       'margin': '0', 'letterSpacing': '4px',
                       'fontWeight': 'bold'}),
        html.P('65 Years of Music\'s Biggest Night  •  1959–2026',
               style={'color': CREAM, 'fontSize': '1.1rem',
                      'marginTop': '8px', 'opacity': '0.8'})
    ]),

    # ---- STAT CARDS ----
    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'gap': '20px',
        'padding': '30px 20px',
        'flexWrap': 'wrap'
    }, children=[
        # Card 1
        html.Div(style={
            'backgroundColor': CARD_BG,
            'borderRadius': '12px',
            'padding': '20px 30px',
            'textAlign': 'center',
            'border': f'1px solid {GOLD}',
            'minWidth': '160px'
        }, children=[
            html.H2(str(total_winners),
                    style={'color': GOLD, 'fontSize': '2.2rem', 'margin': '0'}),
            html.P('Total Winners', style={'color': CREAM, 'margin': '5px 0 0'})
        ]),
        # Card 2
        html.Div(style={
            'backgroundColor': CARD_BG,
            'borderRadius': '12px',
            'padding': '20px 30px',
            'textAlign': 'center',
            'border': f'1px solid {GOLD}',
            'minWidth': '160px'
        }, children=[
            html.H2(str(total_artists),
                    style={'color': GOLD, 'fontSize': '2.2rem', 'margin': '0'}),
            html.P('Unique Artists', style={'color': CREAM, 'margin': '5px 0 0'})
        ]),
        # Card 3
        html.Div(style={
            'backgroundColor': CARD_BG,
            'borderRadius': '12px',
            'padding': '20px 30px',
            'textAlign': 'center',
            'border': f'1px solid {GOLD}',
            'minWidth': '160px'
        }, children=[
            html.H2(years_covered,
                    style={'color': GOLD, 'fontSize': '2.2rem', 'margin': '0'}),
            html.P('Years Covered', style={'color': CREAM, 'margin': '5px 0 0'})
        ]),
        # Card 4
        html.Div(style={
            'backgroundColor': CARD_BG,
            'borderRadius': '12px',
            'padding': '20px 30px',
            'textAlign': 'center',
            'border': f'1px solid {GOLD}',
            'minWidth': '200px'
        }, children=[
            html.H2(f"{top_artist_name}",
                    style={'color': GOLD, 'fontSize': '1.4rem', 'margin': '0'}),
            html.P(f'Most Wins ({top_artist_wins})',
                   style={'color': CREAM, 'margin': '5px 0 0'})
        ]),
    ]),

    # ---- DROPDOWN FILTER ----
    html.Div(style={'padding': '0 30px 10px', 'textAlign': 'center'}, children=[
        html.Label('🔍 Filter Charts by Era:',
                   style={'color': GOLD, 'fontSize': '1rem',
                          'marginRight': '10px'}),
        dcc.Dropdown(
            id='era-filter',
            options=[{'label': 'All Eras', 'value': 'All'}] +
                    [{'label': e, 'value': e}
                     for e in sorted(df_winners['Era'].unique())],
            value='All',
            style={'width': '300px', 'display': 'inline-block',
                   'backgroundColor': CARD_BG, 'color': DARK_BG},
            className='dropdown'
        )
    ]),

    # ---- CHARTS ROW 1 ----
    html.Div(style={
        'display': 'flex',
        'gap': '20px',
        'padding': '10px 30px',
        'flexWrap': 'wrap'
    }, children=[
        html.Div(style={
            'flex': '1', 'minWidth': '400px',
            'backgroundColor': MID_BG,
            'borderRadius': '12px',
            'padding': '10px',
            'border': f'1px solid rgba(255,215,0,0.2)'
        }, children=[dcc.Graph(figure=fig_artists, id='artists-chart')]),

        html.Div(style={
            'flex': '1', 'minWidth': '400px',
            'backgroundColor': MID_BG,
            'borderRadius': '12px',
            'padding': '10px',
            'border': f'1px solid rgba(255,215,0,0.2)'
        }, children=[dcc.Graph(figure=fig_decade, id='decade-chart')])
    ]),

    # ---- CHARTS ROW 2 ----
    html.Div(style={
        'display': 'flex',
        'gap': '20px',
        'padding': '10px 30px 30px',
        'flexWrap': 'wrap'
    }, children=[
        html.Div(style={
            'flex': '2', 'minWidth': '400px',
            'backgroundColor': MID_BG,
            'borderRadius': '12px',
            'padding': '10px',
            'border': f'1px solid rgba(255,215,0,0.2)'
        }, children=[dcc.Graph(figure=fig_big4, id='big4-chart')]),

        html.Div(style={
            'flex': '1', 'minWidth': '300px',
            'backgroundColor': MID_BG,
            'borderRadius': '12px',
            'padding': '10px',
            'border': f'1px solid rgba(255,215,0,0.2)'
        }, children=[dcc.Graph(figure=fig_era, id='era-chart')])
    ]),

    # ---- FOOTER ----
    html.Div(style={
        'textAlign': 'center',
        'padding': '20px',
        'borderTop': f'1px solid {GOLD}',
        'color': CREAM,
        'opacity': '0.6',
        'fontSize': '0.85rem'
    }, children=[
        html.P('Data Source: Grammy Awards Wikipedia • Built with Python, Dash & Plotly')
    ])
])


# CALLBACK: Era Filter

@app.callback(
    Output('decade-chart', 'figure'),
    Output('era-chart',    'figure'),
    Input('era-filter',    'value')
)
def update_charts(selected_era):
    filtered = df_winners if selected_era == 'All' \
               else df_winners[df_winners['Era'] == selected_era]

    # Update decade chart
    fp = df_decade.copy() if selected_era == 'All' else \
         filtered.groupby(['Decade', 'Category']).size()\
                 .reset_index(name='Total_Winners')

    fp2 = fp.pivot_table(index='Decade', columns='Category',
                         values='Total_Winners', fill_value=0).reset_index()

    new_decade = go.Figure()
    for i, cat in enumerate([c for c in fp2.columns if c != 'Decade']):
        new_decade.add_trace(go.Bar(
            x=fp2['Decade'].astype(str), y=fp2[cat],
            name=cat,
            marker_color=cat_colors[i % len(cat_colors)]
        ))
    new_decade.update_layout(
        barmode='stack',
        plot_bgcolor=MID_BG, paper_bgcolor=DARK_BG,
        font_color=CREAM,
        title=dict(text=' Grammy Winners by Decade',
                   font=dict(color=GOLD, size=16)),
        legend=dict(bgcolor=CARD_BG, bordercolor=GOLD,
                    borderwidth=1, font=dict(color=CREAM)),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    # Update era pie
    ec = filtered['Era'].value_counts().reset_index()
    ec.columns = ['Era', 'Count']
    new_era = px.pie(
        ec, names='Era', values='Count',
        color_discrete_sequence=[GOLD, ACCENT, TEAL, PURPLE,
                                  '#B8860B', '#ff6b6b', '#4ecdc4'],
        title=' Wins by Era', hole=0.4
    )
    new_era.update_layout(
        plot_bgcolor=DARK_BG, paper_bgcolor=DARK_BG,
        font_color=CREAM, title_font_color=GOLD,
        title_font_size=16,
        legend=dict(bgcolor=CARD_BG, font=dict(color=CREAM)),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return new_decade, new_era

# RUN

if __name__ == '__main__':
    print("\n Starting Grammy Dashboard...")
    print(" Open your browser")
    app.run(debug=True)