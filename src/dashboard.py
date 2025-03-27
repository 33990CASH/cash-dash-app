import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import sqlite3

# Initialize the Dash app
app = dash.Dash(__name__)


# Load data from SQLite
def load_data():
    conn = sqlite3.connect("../data/cape_coral_econ.db")

    # Load unemployment data
    df_unemployment = pd.read_sql("SELECT * FROM employment", conn)
    df_unemployment['date'] = pd.to_datetime(df_unemployment['date'])

    # Load news data
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

# Create the news table with updated border colors
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
            html.Td(row["news_date"],
                    style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'}),
            html.Td(row["headline"],
                    style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'}),
            html.Td(row["description"],
                    style={'color': '#001737', 'borderBottom': '1px solid #001737', 'padding': '10px'})
        ]) for _, row in df_news.iterrows()
    ])
], style={'width': '100%', 'borderCollapse': 'collapse', 'marginTop': '20px', 'border': '1px solid #001737'})

# Define the layout of the dashboard with the logo centered and larger
app.layout = html.Div([
    # Logo centered and larger
    html.Div([
        html.Img(
            src="https://github.com/CASH3990/CASHassets/blob/main/CCASH_logo_banner.png?raw=true",
            style={
                'width': '600px',  # Increased size
                'height': 'auto',
                'marginBottom': '20px'
            }
        )
    ], style={'textAlign': 'center'}),  # Center the logo
    # Dashboard title
    html.H1("Cape Coral Economic Analysis Dashboard", style={'textAlign': 'center', 'color': '#001737'}),
    # Unemployment chart
    dcc.Graph(figure=fig_unemployment),
    # News table
    html.H2("Recent Economic News", style={'color': '#001737', 'marginTop': '40px'}),
    news_table
], style={'backgroundColor': '#f0eadc', 'padding': '20px', 'minHeight': '100vh'})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)