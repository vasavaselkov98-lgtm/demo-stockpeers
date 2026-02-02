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

# Конфигурация страницы
st.set_page_config(
    page_title="VV Markets Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/vasavaselkov98-lgtm/demo-stockpeers',
        'Report a bug': "https://github.com/vasavaselkov98-lgtm/demo-stockpeers/issues",
        'About': "### Financial Markets Dashboard\nAdvanced peer analysis tool"
    }
)

# Инициализация состояния
initialize_session_state()

# Загрузка CSS
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

# Главная страница
def main():
    # Заголовок с бейджем GitHub
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px;">
        <h1 style="margin: 0; color: #FF4B4B;">📊 VV Markets Dashboard</h1>
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
    
    # Основное содержимое
    render_main_content()

if __name__ == "__main__":
    main()