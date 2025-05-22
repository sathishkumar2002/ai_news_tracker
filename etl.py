import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from rapidfuzz import fuzz

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")
CSV_PATH = "data/news_data.csv"

SEARCH_TERMS = [
    "AI", "artificial intelligence", "machine learning",
    "deep learning", "neural networks", "generative AI",
    "LLM", "chatbot"
]

def fetch_news_for_term(term):
    url = f"https://gnews.io/api/v4/search?q=\"{term}\"&lang=en&max=10&token={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch for {term}: {response.status_code}")
        return []
    articles = response.json().get("articles", [])
    return [
        {
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "publishedAt": a.get("publishedAt"),
            "source": a.get("source", {}).get("name"),
            "image": a.get("image"),
        }
        for a in articles
    ]

def is_similar(title, existing_titles, threshold=50):
    return any(fuzz.token_sort_ratio(title, existing) >= threshold for existing in existing_titles)

def save_to_csv(news_data):
    new_df = pd.DataFrame(news_data)

    if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0:
        try:
            old_df = pd.read_csv(CSV_PATH)
        except Exception as e:
            print(f"⚠️ Warning reading existing CSV: {e}")
            old_df = pd.DataFrame(columns=new_df.columns)
    else:
        old_df = pd.DataFrame(columns=new_df.columns)

    existing_titles = old_df["title"].fillna("").tolist()
    filtered_data = []
    
    # Deduplicate incrementally against existing + filtered
    for row in news_data:
        if not is_similar(row["title"], existing_titles):
            filtered_data.append(row)
            existing_titles.append(row["title"])  # Add to existing_titles immediately

    if not filtered_data:
        print("ℹ️ No new unique articles found.")
        return

    combined_df = pd.concat([old_df, pd.DataFrame(filtered_data)], ignore_index=True)
    combined_df.to_csv(CSV_PATH, index=False)
    print(f"✅ Added {len(filtered_data)} new articles. Total: {len(combined_df)}")

if __name__ == "__main__":
    try:
        all_news = []
        for term in SEARCH_TERMS:
            print(f"🔍 Fetching for: {term}")
            news = fetch_news_for_term(term)
            all_news.extend(news)
            time.sleep(3)  # To respect API rate limits

        save_to_csv(all_news)

    except Exception as e:
        print(f"❌ Error: {e}")
