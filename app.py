# -*- coding: utf-8 -*-
# Financial Markets Dashboard
# Author: Vasiliy Vaselkov
# GitHub: vasavaselkov98-lgtm/demo-stockpeers

import streamlit as st
from modules.ui_components import (
    initialize_session_state,
    render_sidebar,
    render_main_content
)
from modules.data_loader import load_market_data
from modules.charts import create_main_chart, create_comparison_charts

# ÐšÐ¾Ð½Ñ„Ð¸Ð³ÑƒÑ€Ð°Ñ†Ð¸Ñ ÑÑ‚Ñ€Ð°Ð½Ð¸Ñ†Ñ‹
st.set_page_config(
    page_title="VV Markets Dashboard",
    page_icon="ðŸ“ˆ",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/vasavaselkov98-lgtm/demo-stockpeers',
        'Report a bug': "https://github.com/vasavaselkov98-lgtm/demo-stockpeers/issues",
        'About': "### Financial Markets Dashboard\nAdvanced peer analysis tool"
    }
)

# Ð˜Ð½Ð¸Ñ†Ð¸Ð°Ð»Ð¸Ð·Ð°Ñ†Ð¸Ñ ÑÐ¾ÑÑ‚Ð¾ÑÐ½Ð¸Ñ
initialize_session_state()

# Ð—Ð°Ð³Ñ€ÑƒÐ·ÐºÐ° CSS
def load_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .market-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 20px;
        color: white;
        margin: 10px 0;
        transition: transform 0.3s;
    }
    .market-card:hover {
        transform: translateY(-5px);
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Ð“Ð»Ð°Ð²Ð½Ð°Ñ ÑÑ‚Ñ€Ð°Ð½Ð¸Ñ†Ð°
def main():
    # Ð—Ð°Ð³Ð¾Ð»Ð¾Ð²Ð¾Ðº Ñ Ð±ÐµÐ¹Ð´Ð¶ÐµÐ¼ GitHub
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px;">
        <h1 style="margin: 0; color: #FF4B4B;">ðŸ“Š VV Markets Dashboard</h1>
        <a href="https://github.com/vasavaselkov98-lgtm/demo-stockpeers" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-Repository-blue?logo=github" style="height: 28px;">
        </a>
        <span style="background: #4B0082; padding: 5px 15px; border-radius: 20px; font-size: 14px;">
            v1.0.0
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color: #888; font-size: 16px; margin-bottom: 30px;">
    Advanced tool for comparing financial instruments across multiple markets. 
    Real-time and historical analysis with peer comparison.
    </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        render_sidebar()
    
    # ÐžÑÐ½Ð¾Ð²Ð½Ð¾Ðµ ÑÐ¾Ð´ÐµÑ€Ð¶Ð¸Ð¼Ð¾Ðµ
    render_main_content()

if __name__ == "__main__":
    main()
