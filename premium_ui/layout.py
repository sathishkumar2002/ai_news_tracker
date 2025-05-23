
import streamlit as st
from .style import apply_custom_style

def show_premium_dashboard():
    apply_custom_style()
    st.markdown("## ✨ AI News Tracker - Premium Edition")
    st.markdown("Welcome to your daily dose of AI news in a sleek, premium design.")

    with st.container():
        st.markdown("""
        <div class='card'>
            <h4>🚀 Top AI Headline</h4>
            <p>New breakthroughs in multimodal models are reshaping the future of generative AI.</p>
        </div>
        """, unsafe_allow_html=True)
