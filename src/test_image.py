import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout with just an image
app.layout = html.Div([
    html.Img(
        src="/assets/CCASH_logo_square.png",
        style={
            'width': '300px',
            'height': 'auto'
        }
    )
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)