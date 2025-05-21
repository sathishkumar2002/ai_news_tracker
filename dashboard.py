import streamlit as st
import pandas as pd
import os
from datetime import datetime

CSV_PATH = "data/news_data.csv"

st.set_page_config(page_title="AI News Tracker", layout="wide")
st.title("🤖 AI News Tracker")
st.caption("Latest updates on Artificial Intelligence")

if not os.path.exists(CSV_PATH):
    st.warning("No news data found. Run `etl.py` to fetch news.")
    st.stop()

df = pd.read_csv(CSV_PATH, parse_dates=["publishedAt"])
df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors='coerce')
df = df.sort_values("publishedAt", ascending=False)

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    keyword = st.text_input("Search in Title", "")
    start_date = st.date_input("From Date", df["publishedAt"].min().date())
    end_date = st.date_input("To Date", df["publishedAt"].max().date())

# Apply filters
mask = (
    df["publishedAt"].dt.date >= start_date
) & (
    df["publishedAt"].dt.date <= end_date
)

if keyword:
    mask &= df["title"].str.contains(keyword, case=False, na=False)

filtered_df = df[mask]

# Show results
st.write(f"Showing **{len(filtered_df)}** articles")
for _, row in filtered_df.iterrows():
    # Only show image if available
    if pd.notna(row.get("image", None)) and row["image"]:
        st.image(row["image"], width=600)

    # Show title as clickable link
    st.markdown(f"### [{row['title']}]({row['url']})")

    # Show metadata and description
    st.write(f"📰 {row['source']} • 🕒 {row['publishedAt'].strftime('%b %d, %Y')}")
    
    if pd.notna(row.get("description", None)) and row["description"]:
        st.write(row["description"])
    
    st.markdown("---")

