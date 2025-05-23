
import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
            .main { background-color: #f9f9f9; padding: 2rem; }
            .card {
                background-color: #fff;
                padding: 1.5rem;
                border-radius: 20px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin-bottom: 1rem;
            }
            h4 {
                color: #2c3e50;
                font-size: 1.5rem;
            }
            p {
                color: #34495e;
            }
        </style>
    """, unsafe_allow_html=True)
