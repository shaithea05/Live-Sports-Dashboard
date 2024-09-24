import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

title_intro_layout = html.Div([
    html.H1("Welcome to Shaithea and Alessandra's Dashboard!"),
    html.P("This dashboard provides insights into the 2023-24 NCAA basketball season. Use the dropdowns and sliders to filter data and explore different aspects of the season!"),
    html.Hr()  # Horizontal line for separation
])

# Load the data
df = pd.read_csv("NCAA Extended StatsWOSpaces.csv")
df2 = pd.read_csv("NCAA Extended Stats WO Commas.csv")
df3 = pd.read_csv("Efficiency.csv")
df4 = pd.read_csv("Rebounds.csv")

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Scatterplot
scatter_layout = html.Div([
    html.H2('3 Point Shot Attempts vs 3 Point Shots Made in the 2023-24 Season'),
    html.H4('Which teams are best at converting 3FGA to 3FG?', style={'font-weight': 'normal'}),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by 3 Point Shot Attempts:"),
    dcc.RangeSlider(
        id='range-slider',
        min=400, max=1100, step=100,
        marks={400: '400', 500: '500', 600: '600', 700: '700', 800: '800', 900: '900', 1000: '1000', 1100: '1100'},
        value=[400, 1100]
    ),
html.Hr()
])

@app.callback(
    Output("scatter-plot", "figure"),
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    df = pd.read_csv("NCAA Extended Stats WO Commas.csv")
    low, high = slider_range

    mask = (df['3FGA'] > low) & (df['3FGA'] < high)
    fig = px.scatter(
        df[mask], x="3FGA", y="3FG",
        color="Team", size='Avg Opp NET Rank',
        hover_data=['3FG%'])
    return fig

# Bar Graph
bar_layout = html.Div([
    html.H4('Wins & Losses By Conference 2023-24 Season'),
        dcc.Dropdown(
            id="dropdown",
            options=["AAC", "ACC", "America East", "ASUN", "Atlantic 10", "Big 12", "Big East", "Big Sky", "Big South", "Big Ten", "Big West", "CAA", "CUSA", "DI Independent", "Horizon", "Ivy League", "MAAC", "MAC", "MEAC", "Mountain West", "MVC", "MEC", "OVC", "Pac-12", "Patriot", "SEC", "SoCon", "Southland", "Summit League", "Sun Belt", "SWAC", "WAC", "WCC"],
            value="Big 12",    #starting dropdown
            clearable=False,
        ),
        dcc.Graph(id="graph"),
html.Hr()
])

@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"))
def update_bar_chart(Conference):
    df = pd.read_csv("NCAA Extended Stats.csv")
    mask = df["Conference"] == Conference
    fig = px.bar(df[mask], x="Team", y=["Win", "Loss"],
                 color="Win", barmode="group")
    fig.update_yaxes(title_text="Losses")
    return fig

# conference pie chart
pie_chart_layout = html.Div([
html.H4('Breakdown by Conference'),
    html.Div([
        html.Div([
            html.H1(children='Wins and Losses'),
            html.H6('Number of Wins or Losses Summed by conference'),
            dcc.Graph(
                id='graph1',
                # figure=fig1
            ),
        ], className='six columns'),
        html.Div([
            html.H1(children='Breakdown'),
            html.H6('Broken down by AST, APG, 3FG, and 3FGA'),
            dcc.Graph(
                id='graph2',
                # figure = fig2
            ),
        ], className='six columns'),
    ], className='row'),
    html.P("Names:"),
    dcc.Dropdown(id='names',
        options=[{'label': 'Conference', 'value': 'Conference'}, {'label': 'Season', 'value': 'Season'}],
        value='Conference', clearable=False
    ),
    html.P("Values 1:"),
    dcc.Dropdown(id='values1',
        options=[{'label': 'Win', 'value': 'Win'}, {'label': 'Loss', 'value': 'Loss'}],
        value='Win', clearable=False
    ),
    html.P("Values 2:"),
    dcc.Dropdown(id='values2',
        options=[{'label': 'AST', 'value': 'AST'}, {'label': 'APG', 'value': 'APG'},
                 {'label': '3FG', 'value': '3FG'}, {'label': '3FGA', 'value': '3FGA'}],
        value='AST', clearable=False
    ),
html.Hr()
])

@app.callback(
    Output("graph1", "figure"),
    Input("names", "value"),
    Input("values1", "value"))
def generate_chart1(names, values1):
    df = pd.read_csv("NCAA Extended StatsWOSpacesAndCommas.csv")
    fig = px.pie(df, values=values1, names=names)
    return fig

@app.callback(
    Output("graph2", "figure"),
    Input("names", "value"),
    Input("values2", "value"))
def generate_chart2(names, value2):
    df = pd.read_csv("NCAA Extended StatsWOSpacesAndCommas.csv")
    fig = px.pie(df, values=value2, names=names)
    return fig

# efficiency pie chart
efficiency_pie_chart_layout = html.Div([
html.H3('Offensive vs Defensive Efficiency'),
    html.H6('by Region, Conference, and Seed'),
    html.Div([
        html.Div([
            html.H1(children='Offensive Efficiency'),
            dcc.Graph(
                id='graph3',
                # figure=fig1
            ),
        ], className='six columns'),
        html.Div([
            html.H1(children='Defensive Efficiency'),
            dcc.Graph(
                id='graph4',
                # figure = fig2
            ),
        ], className='six columns'),
    ], className='row'),
    html.P("Names:"),
    dcc.Dropdown(id='names2',
        options=[{'label': 'Region', 'value': 'Region'}, {'label': 'Conference', 'value': 'Conference'}, {'label': 'Seed', 'value': 'Seed'} ],
        value='Region', clearable=False
    ),
    html.P("Values 1:"),
    dcc.Dropdown(id='values3',
        options=[{'label': 'Raw Offensive Efficiency', 'value': 'Raw Offensive Efficiency'}],
        value='Raw Offensive Efficiency', clearable=False
    ),
    html.P("Values 2:"),
    dcc.Dropdown(id='values4',
        options=[{'label': 'Raw Defensive Efficiency', 'value': 'Raw Defensive Efficiency'}],
        value='Raw Defensive Efficiency', clearable=False
    ),
    html.Hr()
])

@app.callback(
    Output("graph3", "figure"),
    Input("names2", "value"),
    Input("values3", "value"))
def generate_chart1(names, values1):
    df3 = pd.read_csv("Efficiency.csv")
    fig = px.pie(df3, values=values1, names=names)
    return fig

@app.callback(
    Output("graph4", "figure"),
    Input("names2", "value"),
    Input("values4", "value"))
def generate_chart2(names, value2):
    df3 = pd.read_csv("Efficiency.csv")
    fig = px.pie(df3, values=value2, names=names)
    return fig

# rebounds scatterplot
rebounds_scatter_plot = html.Div([
    html.H4('Rebounds Data'),
    dcc.Graph(id="scatter-plot2"),
    dcc.RangeSlider(
        id='range-slider2',
        min=1, max=600, step=100,
        marks={1: '1', 100: '100', 200: '200', 300: '300', 400: '400', 500: '500', 600:'600'},
        value=[1, 500]
    ),
    html.Hr()
])

@app.callback(
    Output("scatter-plot2", "figure"),
    Input("range-slider2", "value"))
def update_line_chart(slider_range):
    df4 = pd.read_csv("Rebounds.csv")
    low, high = slider_range

    mask = (df4['ORebs'] > low) & (df4['ORebs'] < high)
    fig = px.scatter(
        df4[mask], x="ORebs", y="RPG",
        color="Team", size='GM',
        hover_data=['Team'])
    return fig

app.layout = html.Div([
    title_intro_layout,
    scatter_layout,
    bar_layout,
    pie_chart_layout,
    efficiency_pie_chart_layout,
    rebounds_scatter_plot
])

if __name__ == '__main__':
    app.run_server(debug=True)
