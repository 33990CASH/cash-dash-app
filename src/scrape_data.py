import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import pandas as pd
import re

def scrape_cape_coral_news():
    try:
        # URL for the News / Events page
        url = "https://www.capecoral.gov/edo/news___events.php"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Fetch the page
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the post section containing news items
        post = soup.find("div", class_="post")
        if not post:
            raise ValueError("Post section not found on the page")

        # Extract all <p> tags within the post section
        paragraphs = post.find_all("p")
        if not paragraphs:
            raise ValueError("No paragraphs found in the post section")

        # Extract news items (headline, date, and description)
        scrape_date = datetime.now().strftime("%Y-%m-%d")
        news_list = []
        current_headline = None
        current_date = "N/A"
        current_description = ""

        for p in paragraphs:
            # Check for a headline (in <strong> with font-size: 18px)
            strong = p.find("strong")
            if strong and strong.find("span", style="font-size: 18px;"):
                # If we have a previous news item, save it before starting a new one
                if current_headline:
                    # Clean the description
                    description_text = current_description
                    description_text = re.sub(r"\(\d{1,2}/\d{1,2}/\d{2}\)", "", description_text)  # Remove date
                    description_text = re.sub(r"(Read more|Click here).*$", "", description_text)  # Remove "Read more" or "Click here" links
                    description_text = description_text.strip()
                    news_list.append({
                        "scrape_date": scrape_date,
                        "news_date": current_date,
                        "headline": current_headline,
                        "description": description_text
                    })
                # Extract the new headline
                current_headline = strong.text.strip()
                # Extract the date (e.g., (3/10/25)) using regex
                date_match = re.search(r"\((\d{1,2}/\d{1,2}/\d{2})\)", p.text)
                current_date = date_match.group(1) if date_match else "N/A"
                # Extract the description (text after the headline)
                description_span = p.find_all("span", style="font-size: 18px;")[-1]  # Get the last span (description)
                if description_span:
                    description_text = description_span.text.strip()
                    # Remove the headline if present
                    description_text = description_text.replace(current_headline, "").strip()
                    current_description = description_text
                else:
                    current_description = ""
            else:
                # If no headline, this might be additional text for the current description
                if current_headline:
                    text = p.text.strip()
                    # Exclude text that looks like a new section (e.g., starting with "CAPE CORAL")
                    if text and not text.startswith("CAPE CORAL") and not text.startswith("The city"):
                        current_description += " " + text

        # Add the last news item
        if current_headline:
            description_text = current_description
            description_text = re.sub(r"\(\d{1,2}/\d{1,2}/\d{2}\)", "", description_text)  # Remove date
            description_text = re.sub(r"(Read more|Click here).*$", "", description_text)  # Remove "Read more" or "Click here" links
            description_text = description_text.strip()
            news_list.append({
                "scrape_date": scrape_date,
                "news_date": current_date,
                "headline": current_headline,
                "description": description_text
            })

        if not news_list:
            raise ValueError("No meaningful news items found after parsing")

        # Convert to DataFrame
        df = pd.DataFrame(news_list)

        # Store in SQLite
        conn = sqlite3.connect("../data/cape_coral_econ.db")
        df.to_sql("news", conn, if_exists="replace", index=False)
        conn.close()
        print("News data saved!")
        print("Sample news items:", news_list[:2])  # Debug output

    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
    except ValueError as e:
        print(f"Data error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    scrape_cape_coral_news()