import os
import sqlite3
import pandas as pd
from dash import dcc, html, Dash
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# Load data from SQLite
def load_data():
    # Get the directory of the current script (dashboard.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the database
    db_path = os.path.join(script_dir, "data", "cape_coral_econ.db")
    # Connect to the database
    conn = sqlite3.connect(db_path)
    df_unemployment = pd.read_sql("SELECT * FROM employment", conn)
    df_unemployment['date'] = pd.to_datetime(df_unemployment['date'])
    df_news = pd.read_sql("SELECT * FROM news", conn)
    conn.close()
    return df_unemployment, df_news

# Load the data
df_unemployment, df_news = load_data()

# Create the unemployment chart
fig_unemployment = px.line(
    df_unemployment,
    x="date",
    y="unemployment_rate",
    title="Cape Coral (Lee County) Unemployment Rate (2020-2025)",
    labels={"unemployment_rate": "Unemployment Rate (%)", "date": "Date"}
)
fig_unemployment.update_layout(
    xaxis_title="Date",
    yaxis_title="Unemployment Rate (%)",
    template="plotly_white"
)

# Create the news table
news_table = html.Table([
    html.Thead(
        html.Tr([
            html.Th("Date", style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'}),
            html.Th("Headline", style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'}),
            html.Th("Description", style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'})
        ])
    ),
    html.Tbody([
        html.Tr([
            html.Td(row["news_date"], style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'}),
            html.Td(row["headline"], style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'}),
            html.Td(row["description"], style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'})
        ]) for _, row in df_news.iterrows()
    ])
], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '20px', 'border': '1px solid #001737'})

# Define the layout
app.layout = html.Div([
    html.Div([
        html.Img(
            src=app.get_asset_url('CCASH_logo_banner.png'),
            style={'width': '600px', 'height': 'auto', 'marginBottom': '20px'}
        )
    ], style={'textAlign': 'center'}),
    html.H1("Cape Coral Economic Analysis Dashboard", style={'textAlign': 'center', 'color': '#001737'}),
    dcc.Graph(figure=fig_unemployment),
    html.H2("Recent Economic News", style={'color': '#001737', 'marginTop': '40px'}),
    news_table
], style={'backgroundColor': '#f0eadc', 'padding': '20px', 'minHeight': '100vh'})

# Define the server for Render
server = app.server

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)