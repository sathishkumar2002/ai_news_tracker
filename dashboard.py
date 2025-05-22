import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI News Tracker", layout="wide")
st.title("🧠 AI News Tracker")

# Load CSV
df = pd.read_csv("data/news_data.csv")
df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors='coerce')
df = df.dropna(subset=["publishedAt"])

# Sidebar filters
st.sidebar.markdown("### 🔍 Filters")

min_date = df["publishedAt"].min().date()
max_date = df["publishedAt"].max().date()

start_date = st.sidebar.date_input("From Date", min_value=min_date, value=min_date)
end_date = st.sidebar.date_input("To Date", min_value=min_date, value=max_date)

search_query = st.sidebar.text_input("Search Keyword", "")

# Copy full data
filtered_df = df.copy()

# Apply filters only if they actually change
if start_date != min_date or end_date != max_date:
    filtered_df = filtered_df[
        (filtered_df["publishedAt"].dt.date >= start_date) &
        (filtered_df["publishedAt"].dt.date <= end_date)
    ]

if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False) |
        filtered_df["description"].str.contains(search_query, case=False, na=False)
    ]

# Sort by newest
filtered_df = filtered_df.sort_values(by="publishedAt", ascending=False)

# Show count
st.markdown(f"### Showing {len(filtered_df)} news articles")

# Render each article
for _, row in filtered_df.iterrows():
    if pd.notna(row.get("image")) and row["image"]:
        st.image(row["image"], width=600)

    st.markdown(f"### [{row['title']}]({row['url']})")
    st.write(f"📰 {row['source']} • 🕒 {row['publishedAt'].strftime('%b %d, %Y')}")

    description = row.get("description", "")
    if pd.notna(description) and description.strip():
        st.write(description)

    st.markdown("---")
