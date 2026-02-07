# -*- coding: utf-8 -*-
"""
VV Markets Dashboard Pro - Main Navigation
Streamlit Multi-Page Application with Global State
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="VV Markets Dashboard Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/vasavaselkov98-lgtm/demo-stockpeers',
        'Report a bug': "https://github.com/vasavaselkov98-lgtm/demo-stockpeers/issues",
        'About': """
        # VV Markets Dashboard Pro
        Advanced Financial Markets Control Panel
        
        Version 3.0 | Multi-Page Dashboard with Global State
        """
    }
)

# ==================== ИНИЦИАЛИЗАЦИЯ ГЛОБАЛЬНОГО СОСТОЯНИЯ ====================

def initialize_global_state():
    """Initialize global data state for all pages"""
    if 'global_data' not in st.session_state:
        st.session_state.global_data = {
            'price_data': None,           # Основные ценовые данные
            'tickers': [],                # Список выбранных тикеров
            'market_type': 'Stocks',      # Тип рынка
            'period': '1y',              # Период данных
            'interval': '1d',            # Интервал данных
            'data_loaded': False,        # Флаг загрузки данных
            'last_updated': None,        # Время последнего обновления
            'source_page': None          # Страница-источник данных
        }
    
    # Обратная совместимость со старыми переменными
    if 'price_data' not in st.session_state:
        st.session_state.price_data = None
    if 'market_data' not in st.session_state:
        st.session_state.market_data = None
    if 'selected_tickers' not in st.session_state:
        st.session_state.selected_tickers = []

def sync_old_with_new_state():
    """Синхронизировать старые переменные с новым глобальным state"""
    if st.session_state.global_data['data_loaded']:
        st.session_state.price_data = st.session_state.global_data['price_data']
        st.session_state.market_data = st.session_state.global_data['price_data']
        st.session_state.selected_tickers = st.session_state.global_data['tickers']

def update_global_state(price_data, tickers, market_type, period, interval, source_page="Dashboard"):
    """Обновить глобальное состояние данных"""
    st.session_state.global_data.update({
        'price_data': price_data,
        'tickers': tickers,
        'market_type': market_type,
        'period': period,
        'interval': interval,
        'data_loaded': True,
        'last_updated': datetime.now(),
        'source_page': source_page
    })
    
    # Синхронизировать со старыми переменными
    sync_old_with_new_state()

def clear_global_state():
    """Очистить глобальное состояние"""
    st.session_state.global_data = {
        'price_data': None,
        'tickers': [],
        'market_type': 'Stocks',
        'period': '1y',
        'interval': '1d',
        'data_loaded': False,
        'last_updated': None,
        'source_page': None
    }
    
    # Очистить старые переменные
    st.session_state.price_data = None
    st.session_state.market_data = None
    st.session_state.selected_tickers = []

# ==================== CSS СТИЛИ ====================

def apply_custom_styles():
    """Apply custom CSS styles"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        text-align: center;
        font-weight: 700;
    }
    .tagline {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .data-status-card {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        border-radius: 10px;
        padding: 1.5rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .stats-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    .nav-card {
        border-radius: 10px;
        padding: 1.5rem;
        height: 180px;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    .nav-card:hover {
        transform: translateY(-3px);
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background-color: #4CAF50;
    }
    .status-offline {
        background-color: #f44336;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== КОМПОНЕНТЫ ИНТЕРФЕЙСА ====================

def create_data_status_panel():
    """Панель статуса данных"""
    if st.session_state.global_data['data_loaded']:
        global_data = st.session_state.global_data
        
        st.markdown("""
        <div class='data-status-card'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <h3 style='margin: 0; color: white;'>📊 Active Data Session</h3>
                    <p style='margin: 5px 0 0 0; opacity: 0.9; font-size: 0.9rem;'>
                        Data loaded and synchronized across all pages
                    </p>
                </div>
                <span class='status-indicator status-online'></span>
            </div>
            
            <div style='margin-top: 15px; display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px;'>
                <div>
                    <div style='font-size: 0.8rem; opacity: 0.8;'>Market Type</div>
                    <div style='font-weight: 600;'>{}</div>
                </div>
                <div>
                    <div style='font-size: 0.8rem; opacity: 0.8;'>Tickers</div>
                    <div style='font-weight: 600;'>{}</div>
                </div>
                <div>
                    <div style='font-size: 0.8rem; opacity: 0.8;'>Period</div>
                    <div style='font-weight: 600;'>{}</div>
                </div>
                <div>
                    <div style='font-size: 0.8rem; opacity: 0.8;'>Source</div>
                    <div style='font-weight: 600;'>{}</div>
                </div>
            </div>
        </div>
        """.format(
            global_data['market_type'],
            ', '.join(global_data['tickers'][:3]) + ('...' if len(global_data['tickers']) > 3 else ''),
            global_data['period'],
            global_data['source_page'] or 'Dashboard'
        ), unsafe_allow_html=True)
        
        # Кнопки управления данными
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📊 Dashboard", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Dashboard.py")
        with col2:
            if st.button("📈 Technical", use_container_width=True):
                st.switch_page("pages/2_Technical.py")
        with col3:
            if st.button("⚠️ Risk", use_container_width=True):
                st.switch_page("pages/4_Risk.py")
        with col4:
            if st.button("🧹 Clear", use_container_width=True, type="secondary"):
                clear_global_state()
                st.rerun()
        return True
    return False

def create_quick_navigation():
    """Create quick navigation cards"""
    st.markdown("""
    <h1 class='main-header'>🚀 VV Markets Dashboard Pro</h1>
    <div class='tagline'>Professional Multi-Page Financial Analysis Platform</div>
    """, unsafe_allow_html=True)
    
    # Панель статуса данных (если данные загружены)
    has_data = create_data_status_panel()
    
    # Navigation grid
    st.markdown("### 🎯 Module Navigation")
    
    # Navigation modules with your actual page names
    nav_modules = [
        {
            "title": "📊 Market Dashboard",
            "page": "1_Dashboard.py",
            "description": "Load market data, charts, and analysis tools",
            "color": "#1f77b4",
            "is_data_source": True
        },
        {
            "title": "🔧 Technical Analysis",
            "page": "2_Technical.py",
            "description": "Technical indicators, RSI, moving averages",
            "color": "#ff7f0e",
            "is_data_source": False
        },
        {
            "title": "⚖️ Portfolio Optimization",
            "page": "3_Portfolio.py",
            "description": "Portfolio allocation and optimization",
            "color": "#2ca02c",
            "is_data_source": False
        },
        {
            "title": "⚠️ Risk Analysis",
            "page": "4_Risk.py",
            "description": "VaR, stress testing, risk metrics",
            "color": "#d62728",
            "is_data_source": False
        },
        {
            "title": "🧠 Indicators Library",
            "page": "6_Indicators.py",
            "description": "Custom indicators and tools",
            "color": "#9467bd",
            "is_data_source": False
        },
        {
            "title": "📚 Documentation",
            "page": "5_Documentation.py",
            "description": "User guides and tutorials",
            "color": "#8c564b",
            "is_data_source": False
        }
    ]
    
    # Create navigation grid
    cols = st.columns(3)
    for idx, module in enumerate(nav_modules):
        with cols[idx % 3]:
            # Card style
            card_style = f"""
            <div style='
                background-color: {module['color']}15;
                border: 2px solid {module['color']};
                border-radius: 10px;
                padding: 1.5rem;
                height: 180px;
                margin-bottom: 1rem;
            '>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{module['title'].split()[0]}</div>
                <div style='font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;'>
                    {module['title'].split()[1:]}
                </div>
                <div style='font-size: 0.85rem; color: #666; line-height: 1.4;'>
                    {module['description']}
                </div>
            </div>
            """
            st.markdown(card_style, unsafe_allow_html=True)
            
            # Data indicator
            if has_data and not module['is_data_source']:
                st.caption("✅ Uses global data")
            
            # Navigation button
            if st.button(f"Open {module['title'].split()[1]}", 
                        key=f"nav_{idx}",
                        use_container_width=True):
                st.switch_page(f"pages/{module['page']}")

def create_sidebar():
    """Create sidebar with quick settings"""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/stock-share.png", width=80)
        st.markdown("<h2 style='text-align: center;'>VV Markets Pro</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Data Status
        st.subheader("💾 Data Status")
        
        if st.session_state.global_data['data_loaded']:
            global_data = st.session_state.global_data
            st.success(f"✅ {len(global_data['tickers'])} tickers loaded")
            st.caption(f"Market: {global_data['market_type']}")
            st.caption(f"Period: {global_data['period']}")
            
            # Quick data actions
            if st.button("📊 Use in Dashboard", use_container_width=True):
                st.switch_page("pages/1_Dashboard.py")
            if st.button("⚠️ Analyze Risk", use_container_width=True):
                st.switch_page("pages/4_Risk.py")
            if st.button("🧹 Clear Data", use_container_width=True, type="secondary"):
                clear_global_state()
                st.rerun()
        else:
            st.warning("No data loaded")
            if st.button("📥 Load Data", use_container_width=True, type="primary"):
                st.switch_page("pages/1_Dashboard.py")
        
        st.markdown("---")
        
        # Quick Settings
        st.subheader("⚙️ Settings")
        
        data_source = st.selectbox(
            "Data Source",
            ["Yahoo Finance", "Demo Data", "Custom"],
            index=0
        )
        
        auto_refresh = st.checkbox("Auto-refresh data", value=False)
        
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "System"],
            index=0
        )
        
        st.markdown("---")
        
        # System Info
        st.subheader("📊 System Info")
        
        st.caption(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.caption(f"🌐 Source: {data_source}")
        st.caption("✅ All systems operational")
        
        st.markdown("---")
        
        # Quick Links
        st.subheader("🔗 Quick Links")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Docs", use_container_width=True):
                st.switch_page("pages/5_Documentation.py")
        with col2:
            if st.button("🐛 Issues", use_container_width=True):
                st.markdown("[GitHub Issues](https://github.com/vasavaselkov98-lgtm/demo-stockpeers/issues)")

def create_how_to_section():
    """Секция с инструкциями"""
    with st.expander("📖 How to Use Global Data Sync", expanded=False):
        st.markdown("""
        ### 🔄 Global Data Sync System
        
        **Workflow:**
        1. **Load data in Dashboard** (pages/1_Dashboard.py)
        2. **Data automatically syncs** to all other pages
        3. **Navigate to any page** - data will be available
        4. **Analyze from different perspectives** without re-loading
        
        **Pages that use global data:**
        - ✅ **Dashboard** - Main data loading and charts
        - ✅ **Technical Analysis** - Indicators on loaded data
        - ✅ **Portfolio Optimization** - Portfolio with loaded tickers
        - ✅ **Risk Analysis** - Risk metrics on current data
        
        **Independent pages:**
        - 📚 **Documentation** - User guides
        - 🧠 **Indicators Library** - Custom tools
        
        **Example:**
        ```
        1. Dashboard → Load AAPL, MSFT, GOOGL
        2. Technical → Analyze RSI and trends
        3. Portfolio → Optimize weights
        4. Risk → Calculate VaR
        ```
        All using the **same data** loaded once!
        """)

# ==================== ГЛАВНАЯ ФУНКЦИЯ ====================

def main():
    """Main application function"""
    
    # Инициализация глобального состояния
    initialize_global_state()
    
    # Apply styles
    apply_custom_styles()
    
    # Create sidebar
    create_sidebar()
    
    # Main content
    create_quick_navigation()
    
    # How-to section
    create_how_to_section()
    
    # Footer
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d')}")
    with col2:
        if st.session_state.global_data['data_loaded']:
            ticker_count = len(st.session_state.global_data['tickers'])
            st.caption(f"📊 {ticker_count} active tickers")
        else:
            st.caption("📊 No data loaded")
    with col3:
        st.caption("🚀 VV Markets Pro v3.0")

# ==================== ЭКСПОРТ ФУНКЦИЙ ДЛЯ ДРУГИХ СТРАНИЦ ====================

def get_global_data():
    """Get global data state"""
    return st.session_state.global_data

def is_data_loaded():
    """Check if data is loaded"""
    return st.session_state.global_data['data_loaded']

def get_price_data():
    """Get price data"""
    return st.session_state.global_data['price_data']

def get_tickers():
    """Get tickers list"""
    return st.session_state.global_data['tickers']

def get_market_info():
    """Get market information"""
    return {
        'type': st.session_state.global_data['market_type'],
        'period': st.session_state.global_data['period'],
        'interval': st.session_state.global_data['interval']
    }

# Если файл запущен напрямую
if __name__ == "__main__":
    main()
