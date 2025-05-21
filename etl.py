import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")
SEARCH_QUERY = "artificial intelligence"
CSV_PATH = "data/news_data.csv"

def fetch_ai_news():
    url = f"https://gnews.io/api/v4/search?q={SEARCH_QUERY}&lang=en&max=10&token={API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch news: {response.status_code}, {response.text}")
    
    articles = response.json().get("articles", [])
    
    news_data = []
    for article in articles:
        news_data.append({
            "title": article.get("title"),
            "description": article.get("description"), 
            "url": article.get("url"),
            "publishedAt": article.get("publishedAt"),
            "source": article.get("source", {}).get("name"),
            "image": article.get("urlToImage"),
        })

    return news_data

def save_to_csv(news_data):
    # Convert new data to DataFrame
    new_df = pd.DataFrame(news_data)

    if os.path.exists(CSV_PATH):
        # Load old data
        old_df = pd.read_csv(CSV_PATH)
        # Combine and drop duplicates based on title + publishedAt
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset=["title", "publishedAt"], inplace=True)
    else:
        combined_df = new_df

    # Save back to CSV
    combined_df.to_csv(CSV_PATH, index=False)
    print(f"✅ Saved {len(combined_df)} total articles to {CSV_PATH}")

if __name__ == "__main__":
    try:
        news = fetch_ai_news()
        save_to_csv(news)
    except Exception as e:
        print(f"❌ Error: {e}")
