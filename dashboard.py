import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import webbrowser
import os

# Page configuration
st.set_page_config(
    page_title="AI NEWS TRACKER | Real-time AI News Dashboard",
    layout="wide",
    page_icon="🧠"
)

# Global CSS styling with added center alignment for main content
st.markdown("""
    <style>
        :root {
            --primary: #2a3f5f;
            --secondary: #6c757d;
            --background: #f8f9fa;
            --card-bg: transparent;
            --text: #333333;
            --accent: #f39c12;
        }

        [data-theme="dark"] {
            --primary: #f0f2f6;
            --secondary: #adb5bd;
            --background: #0e1117;
            --card-bg: transparent;
            --text: #f0f2f6;
            --accent: #f39c12;
        }

        /* Center main content */
        .main-content {
            text-align: center;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }

        .article-container {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e0e0e0;
            text-align: center; /* center article text */
        }

        .article-image {
            border-radius: 8px;
            margin-bottom: 15px;
            max-height: 400px;
            object-fit: contain;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .source-time {
            color: var(--secondary);
            margin-bottom: 10px;
            font-size: 0.9em;
        }

        .article-description {
            margin-top: 10px;
            line-height: 1.5;
        }

        .sidebar-header {
            font-weight: 600;
            color: var(--accent);
            margin: 1rem 0 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sidebar-link {
            display: block;
            padding: 0.5rem 0;
            color: var(--text);
            text-decoration: none;
            transition: all 0.2s;
        }

        .sidebar-link:hover {
            color: var(--accent);
            transform: translateX(3px);
        }

        .payment-btn {
            width: 100%;
            padding: 0.6rem;
            margin: 0.3rem 0;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            background: var(--card-bg);
            color: var(--text);
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }

        .payment-btn:hover {
            background: var(--accent);
            color: white;
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/news_data.csv")
        df["publishedAt"] = pd.to_datetime(df["publishedAt"], utc=True)
        return df.sort_values("publishedAt", ascending=False)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


def render_sidebar_extras():
    with st.sidebar:
        st.markdown("---")

        # Bug Report Section
        st.markdown('<div class="sidebar-header">🐞 Bug Reports</div>', unsafe_allow_html=True)
        st.markdown("""
            Found an issue? Please report it:

            <a href="mailto:skumar300702@gmail.com?subject=[BUG] AI News Tracker" class="sidebar-link">
                ✉️ Email Bug Report
            </a>

            <a href="https://www.linkedin.com/in/sathish-kumar-s-0671111ab/" class="sidebar-link" target="_blank">
                🔗 Contact via LinkedIn
            </a>
        """, unsafe_allow_html=True)

        # Contact Info Section
        st.markdown('<div class="sidebar-header">📬 Contact Info</div>', unsafe_allow_html=True)
        st.markdown("""
            <a href="mailto:skumar300702@gmail.com" class="sidebar-link">
                ✉️ skumar300702@gmail.com
            </a>

            <a href="https://www.linkedin.com/in/sathish-kumar-s-0671111ab/" class="sidebar-link" target="_blank">
                🔗 LinkedIn Profile
            </a>
        """, unsafe_allow_html=True)

        # Support Section (Reveals UPI on click)
        st.markdown('<div class="sidebar-header">❤️ Support This Project</div>', unsafe_allow_html=True)
        support_clicked = st.button("💖 Support")

        if support_clicked:
            st.markdown("Choose a method to support this project:")
            if st.button("📱 Pay via UPI (Mobile Only)", use_container_width=True):
                webbrowser.open("upi://pay?pa=8270155541@amazonpay&pn=AI%20News%20Tracker&mc=0000&mode=02")

            st.markdown(
                "<div style='font-size: 0.8em; text-align: center; opacity: 0.7;'>"
                "If UPI link doesn't open, you can manually send to <code>8270155541@amazonpay</code> via your UPI app."
                "</div>", unsafe_allow_html=True
            )


def main():
    image_path = "assets/AINEWSTRACKER_IMAGE.png"
    if os.path.exists(image_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_path, width=400)
            st.markdown(
                '<div style="text-align: center; color: var(--secondary); font-size: 1rem; margin-top: 0.3rem;">'
                'Latest artificial intelligence news</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown(
            '<h1 style="text-align: center;">AI NEWS TRACKER</h1>'
            '<div style="text-align: center; color: var(--secondary); font-size: 1rem;">'
            'Latest artificial intelligence news</div>',
            unsafe_allow_html=True
        )

    # Load data
    df = load_data()

    if not df.empty:
        with st.sidebar:
            st.subheader("🔍 Filters")

            min_date = st.date_input("From date", value=None)
            max_date = st.date_input("To date", value=None)

            sources = ["All sources"] + sorted(df["source"].unique().tolist())
            selected_source = st.selectbox("Filter by source", sources, index=0)

            search_query = st.text_input("Search articles")

        # Apply filters
        filtered_df = df.copy()

        if min_date:
            filtered_df = filtered_df[filtered_df["publishedAt"].dt.date >= min_date]
        if max_date:
            filtered_df = filtered_df[filtered_df["publishedAt"].dt.date <= max_date]
        if selected_source != "All sources":
            filtered_df = filtered_df[filtered_df["source"] == selected_source]
        if search_query:
            filtered_df = filtered_df[
                filtered_df["title"].str.contains(search_query, case=False) |
                filtered_df["description"].str.contains(search_query, case=False)
            ]

        filtered_df = filtered_df.sort_values(by="publishedAt", ascending=False)

        #st.markdown(f"**Showing {len(filtered_df)} news articles**")
        st.markdown("---")

        for _, row in filtered_df.iterrows():
            with st.container():
                if pd.notna(row.get("image")) and str(row["image"]).startswith('http'):
                    st.markdown(
                        f'<div style="text-align: center;">'
                        f'<img src="{row["image"]}" width="600" style="max-width: 100%; height: auto; border-radius: 8px;" />'
                        f'</div>', unsafe_allow_html=True
    )

                st.markdown(f'<h3 style="text-align: center;">'
                            f'<a href="{row["url"]}" target="_blank" style="color:inherit; text-decoration:none;">'
                            f'{row["title"]}</a></h3>', unsafe_allow_html=True)

                st.markdown(
                    f'<div style="text-align: center; color: var(--secondary); font-size: 0.9em;">'
                    f'📰 {row["source"]} • 🕒 {row["publishedAt"].strftime("%b %d, %Y")}'
                    f'</div>', unsafe_allow_html=True
                )

                description = row.get("description", "")
                if pd.notna(description) and description.strip():
                    st.markdown(f'<p style="text-align: center; margin-top: 10px; line-height: 1.5;">'
                                f'{description}</p>', unsafe_allow_html=True)

                st.markdown("---")

    else:
        st.warning("No news articles found")

    render_sidebar_extras()


if __name__ == "__main__":
    main()
