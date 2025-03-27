import pandas as pd
import plotly.express as px
import sqlite3

def visualize_unemployment():
    try:
        # Load data from SQLite
        conn = sqlite3.connect("../data/cape_coral_econ.db")
        df = pd.read_sql("SELECT * FROM employment", conn)
        conn.close()

        # Ensure data is not empty
        if df.empty:
            raise ValueError("No data found in the employment table")

        # Create a line chart
        fig = px.line(
            df,
            x="date",
            y="unemployment_rate",
            title="Cape Coral (Lee County) Unemployment Rate (2020-2025)",
            labels={"unemployment_rate": "Unemployment Rate (%)", "date": "Date"}
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Unemployment Rate (%)",
            template="plotly_white"
        )

        # Show the plot (opens in browser)
        fig.show()
        print("Visualization created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    visualize_unemployment()