import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AI News Tracker", layout="wide")
st.title("🧠 AI News Tracker")

# Load CSV
df = pd.read_csv("data/news_data.csv")

# Parse date column (standardized ISO 8601 format from ETL)
df["publishedAt"] = pd.to_datetime(df["publishedAt"], utc=True, errors='coerce')
df = df.dropna(subset=["publishedAt"])  # Remove rows with invalid/missing dates

# Sidebar filters
st.sidebar.markdown("### 🔍 Filters")

min_date = df["publishedAt"].min().date()
max_date = df["publishedAt"].max().date()

start_date = st.sidebar.date_input("From Date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("To Date", value=max_date, min_value=min_date, max_value=max_date)

search_query = st.sidebar.text_input("Search Keyword", "")

# Apply filters
filtered_df = df.copy()

# Apply date filter only if changed
if start_date != min_date or end_date != max_date:
    filtered_df = filtered_df[
        (filtered_df["publishedAt"].dt.date >= start_date) &
        (filtered_df["publishedAt"].dt.date <= end_date)
    ]

# Apply keyword filter
if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False) |
        filtered_df["description"].str.contains(search_query, case=False, na=False)
    ]

# Sort by date
filtered_df = filtered_df.sort_values(by="publishedAt", ascending=False)

# Show count
st.markdown(f"### Showing {len(filtered_df)} news articles")

# Display articles
for _, row in filtered_df.iterrows():
    if pd.notna(row.get("image")) and row["image"]:
        st.image(row["image"], width=600)

    st.markdown(f"### [{row['title']}]({row['url']})")
    st.write(f"📰 {row['source']} • 🕒 {row['publishedAt'].strftime('%b %d, %Y')}")

    description = row.get("description", "")
    if pd.notna(description) and description.strip():
        st.write(description)

    st.markdown("---")
