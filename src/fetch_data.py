import requests
import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("FRED_API_KEY")
if not API_KEY:
    raise ValueError("FRED_API_KEY not found in .env file")

# FRED series: Lee County unemployment rate
SERIES_ID = "FLLEEC7URN"


def fetch_employment_data():
    try:
        # Set start date (last 5 years), no end date to get latest available data
        start_date = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={SERIES_ID}&api_key={API_KEY}&observation_start={start_date}&limit=1000&sort_order=asc&file_type=json"
        print("Request URL:", url)

        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        response_data = response.json()
        print("API Response:", response_data)  # Debug output

        if "observations" not in response_data:
            raise KeyError(f"'observations' key not found in response: {response_data}")

        data = response_data["observations"]
        if not data:
            raise ValueError("No observations found for the given date range")

        df = pd.DataFrame(data)[["date", "value"]].rename(columns={"value": "unemployment_rate"})
        df["date"] = pd.to_datetime(df["date"])
        df["unemployment_rate"] = df["unemployment_rate"].astype(float)

        # Store in SQLite
        conn = sqlite3.connect("../data/cape_coral_econ.db")
        df.to_sql("employment", conn, if_exists="replace", index=False)
        conn.close()
        print("Employment data saved!")
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        print(f"Response Text: {response.text if 'response' in locals() else 'No response'}")
    except KeyError as e:
        print(f"Key error: {e}")
    except ValueError as e:
        print(f"Data error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    fetch_employment_data()