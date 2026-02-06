"""
Менеджер данных для всех типов финансовых инструментов
Акции, Фьючерсы, Товары, Индексы, Криптовалюта, Форекс
"""
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import streamlit as st
from datetime import datetime, timedelta
import cachetools


class DataManager:
    """Управление данными различных финансовых инструментов"""
    
    def __init__(self):
        self.cache = cachetools.TTLCache(maxsize=100, ttl=300)  # Кэш на 5 минут
        
        # Конфигурация инструментов по типам
        self.instrument_config = {
            'stocks': {
                'name': 'Акции',
                'icon': '📈',
                'tickers': {
                    'AAPL': 'Apple Inc.',
                    'GOOGL': 'Alphabet Inc.',
                    'MSFT': 'Microsoft',
                    'TSLA': 'Tesla Inc.',
                    'NVDA': 'NVIDIA Corp',
                    'AMZN': 'Amazon.com Inc.',
                    'META': 'Meta Platforms',
                    'JPM': 'JPMorgan Chase',
                    'JNJ': 'Johnson & Johnson',
                    'V': 'Visa Inc.',
                    'WMT': 'Walmart',
                    'PG': 'Procter & Gamble',
                    'MA': 'Mastercard',
                    'DIS': 'Walt Disney',
                    'BAC': 'Bank of America'
                }
            },
            'futures': {
                'name': 'Фьючерсы',
                'icon': '⚡',
                'tickers': {
                    'ES=F': 'S&P 500 E-mini',
                    'NQ=F': 'NASDAQ E-mini',
                    'YM=F': 'Dow Jones E-mini',
                    'CL=F': 'Crude Oil WTI',
                    'GC=F': 'Gold',
                    'SI=F': 'Silver',
                    'HG=F': 'Copper',
                    'NG=F': 'Natural Gas',
                    'ZC=F': 'Corn',
                    'ZS=F': 'Soybeans',
                    'ZW=F': 'Wheat',
                    'LE=F': 'Live Cattle',
                    'HE=F': 'Lean Hogs',
                    'KC=F': 'Coffee'
                }
            },
            'commodities': {
                'name': 'Товары',
                'icon': '🛢️',
                'tickers': {
                    'GC=F': 'Gold Futures',
                    'SI=F': 'Silver Futures',
                    'PL=F': 'Platinum Futures',
                    'PA=F': 'Palladium Futures',
                    'HG=F': 'Copper Futures',
                    'CL=F': 'Crude Oil WTI',
                    'BZ=F': 'Brent Crude Oil',
                    'NG=F': 'Natural Gas',
                    'ZC=F': 'Corn',
                    'ZS=F': 'Soybeans',
                    'ZW=F': 'Wheat',
                    'SB=F': 'Sugar',
                    'KC=F': 'Coffee',
                    'CT=F': 'Cotton',
                    'OJ=F': 'Orange Juice'
                }
            },
            'indices': {
                'name': 'Индексы',
                'icon': '📊',
                'tickers': {
                    '^GSPC': 'S&P 500',
                    '^IXIC': 'NASDAQ Composite',
                    '^DJI': 'Dow Jones Industrial',
                    '^RUT': 'Russell 2000',
                    '^FTSE': 'FTSE 100',
                    '^N225': 'Nikkei 225',
                    '^HSI': 'Hang Seng',
                    '^AXJO': 'ASX 200',
                    '^VIX': 'CBOE Volatility Index',
                    '^TNX': '10-Year Treasury Yield',
                    '^FVX': '5-Year Treasury Yield',
                    '^TYX': '30-Year Treasury Yield',
                    '^GDAXI': 'DAX (Germany)',
                    '^FCHI': 'CAC 40 (France)'
                }
            },
            'crypto': {
                'name': 'Криптовалюта',
                'icon': '₿',
                'tickers': {
                    'BTC-USD': 'Bitcoin USD',
                    'ETH-USD': 'Ethereum USD',
                    'BNB-USD': 'Binance Coin USD',
                    'XRP-USD': 'Ripple USD',
                    'ADA-USD': 'Cardano USD',
                    'SOL-USD': 'Solana USD',
                    'DOT-USD': 'Polkadot USD',
                    'DOGE-USD': 'Dogecoin USD',
                    'AVAX-USD': 'Avalanche USD',
                    'MATIC-USD': 'Polygon USD',
                    'SHIB-USD': 'Shiba Inu USD',
                    'TRX-USD': 'TRON USD',
                    'UNI-USD': 'Uniswap USD',
                    'LINK-USD': 'Chainlink USD',
                    'LTC-USD': 'Litecoin USD'
                }
            },
            'forex': {
                'name': 'Форекс',
                'icon': '💱',
                'tickers': {
                    'EURUSD=X': 'EUR/USD',
                    'GBPUSD=X': 'GBP/USD',
                    'USDJPY=X': 'USD/JPY',
                    'USDCHF=X': 'USD/CHF',
                    'AUDUSD=X': 'AUD/USD',
                    'USDCAD=X': 'USD/CAD',
                    'NZDUSD=X': 'NZD/USD',
                    'EURGBP=X': 'EUR/GBP',
                    'EURJPY=X': 'EUR/JPY',
                    'GBPJPY=X': 'GBP/JPY',
                    'AUDJPY=X': 'AUD/JPY',
                    'EURCAD=X': 'EUR/CAD',
                    'GBPAUD=X': 'GBP/AUD',
                    'USDCNY=X': 'USD/CNY',
                    'USDKRW=X': 'USD/KRW'
                }
            },
            'etfs': {
                'name': 'ETF',
                'icon': '📦',
                'tickers': {
                    'SPY': 'SPDR S&P 500 ETF',
                    'QQQ': 'Invesco QQQ Trust',
                    'IVV': 'iShares Core S&P 500 ETF',
                    'VTI': 'Vanguard Total Stock Market ETF',
                    'VOO': 'Vanguard S&P 500 ETF',
                    'ARKK': 'ARK Innovation ETF',
                    'GLD': 'SPDR Gold Shares',
                    'SLV': 'iShares Silver Trust',
                    'USO': 'United States Oil Fund',
                    'TLT': 'iShares 20+ Year Treasury Bond ETF',
                    'IWM': 'iShares Russell 2000 ETF',
                    'EEM': 'iShares MSCI Emerging Markets ETF',
                    'VGK': 'Vanguard FTSE Europe ETF',
                    'BND': 'Vanguard Total Bond Market ETF',
                    'LQD': 'iShares iBoxx $ Investment Grade Corporate Bond ETF'
                }
            }
        }
    
    @st.cache_data(ttl=300, show_spinner="Загрузка данных...")
    def fetch_data(_self, ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
        """Загрузка данных для тикера"""
        
        cache_key = f"{ticker}_{period}_{interval}"
        if cache_key in _self.cache:
            return _self.cache[cache_key]
        
        try:
            # Для индексов используем особый подход
            if ticker.startswith('^'):
                stock = yf.Ticker(ticker)
                data = stock.history(period=period, interval=interval, auto_adjust=False)
            else:
                # Для остальных инструментов
                stock = yf.Ticker(ticker)
                data = stock.history(period=period, interval=interval)
            
            # Если данные пустые, пробуем альтернативный подход
            if data.empty:
                end_date = datetime.now()
                
                # Определяем начальную дату на основе периода
                period_map = {
                    "1d": 1, "5d": 5, "1mo": 30, "3mo": 90,
                    "6mo": 180, "1y": 365, "2y": 730, "5y": 1825, "10y": 3650
                }
                
                days = period_map.get(period, 365)
                start_date = end_date - timedelta(days=days)
                
                data = yf.download(ticker, start=start_date, end=end_date, 
                                 interval=interval, progress=False)
            
            # Добавляем расчетные поля
            if not data.empty:
                data = _self._calculate_technical_fields(data)
                _self.cache[cache_key] = data
            
            return data
            
        except Exception as e:
            st.warning(f"Ошибка загрузки данных для {ticker}: {str(e)}")
            return pd.DataFrame()
    
    def _calculate_technical_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Расчет технических полей"""
        if df.empty:
            return df
        
        # Базовые расчеты
        df['Returns'] = df['Close'].pct_change()
        df['Cumulative_Returns'] = (1 + df['Returns']).cumprod() - 1
        
        # Волатильность
        df['Volatility'] = df['Returns'].rolling(window=20).std() * np.sqrt(252)
        
        # Скользящие средние
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        return df
    
    def get_instrument_types(self) -> List[Dict]:
        """Получить список типов инструментов"""
        return [
            {
                'id': key,
                'name': config['name'],
                'icon': config['icon'],
                'tickers': list(config['tickers'].keys())
            }
            for key, config in self.instrument_config.items()
        ]
    
    def get_tickers_by_type(self, instrument_type: str) -> List[str]:
        """Получить тикеры по типу инструмента"""
        if instrument_type in self.instrument_config:
            return list(self.instrument_config[instrument_type]['tickers'].keys())
        return []
    
    def get_instrument_name(self, ticker: str) -> str:
        """Получить название инструмента по тикеру"""
        for config in self.instrument_config.values():
            if ticker in config['tickers']:
                return config['tickers'][ticker]
        return ticker
    
    def get_instrument_type(self, ticker: str) -> Optional[str]:
        """Получить тип инструмента по тикеру"""
        for instr_type, config in self.instrument_config.items():
            if ticker in config['tickers']:
                return instr_type
        return None
    
    def search_instruments(self, query: str, max_results: int = 10) -> List[Dict]:
        """Поиск инструментов"""
        results = []
        query_lower = query.lower()
        
        for instr_type, config in self.instrument_config.items():
            for ticker, name in config['tickers'].items():
                if (query_lower in ticker.lower() or query_lower in name.lower()):
                    results.append({
                        'ticker': ticker,
                        'name': name,
                        'type': instr_type,
                        'type_name': config['name'],
                        'icon': config['icon']
                    })
                    
                    if len(results) >= max_results:
                        return results
        
        return results
    
    def get_multiple_data(self, tickers: List[str], period: str = "1y", 
                         interval: str = "1d") -> Dict[str, pd.DataFrame]:
        """Загрузка данных для нескольких тикеров"""
        data_dict = {}
        
        for ticker in tickers:
            data = self.fetch_data(ticker, period, interval)
            if data is not None and not data.empty:
                data_dict[ticker] = data
        
        return data_dict
    
    def calculate_correlation_matrix(self, tickers: List[str], 
                                   period: str = "1y") -> pd.DataFrame:
        """Расчет матрицы корреляции"""
        data_dict = self.get_multiple_data(tickers, period)
        
        if not data_dict or len(data_dict) < 2:
            return pd.DataFrame()
        
        # Собираем доходности
        returns_series = []
        
        for ticker, data in data_dict.items():
            if 'Returns' in data.columns:
                returns_series.append(data['Returns'].rename(ticker))
        
        if len(returns_series) < 2:
            return pd.DataFrame()
        
        # Создаем DataFrame с доходностями
        returns_df = pd.concat(returns_series, axis=1)
        returns_df = returns_df.dropna()
        
        # Рассчитываем корреляцию
        correlation_matrix = returns_df.corr()
        
        return correlation_matrix


# Глобальный экземпляр менеджера данных
_data_manager = None

def get_data_manager() -> DataManager:
    """Получить глобальный экземпляр менеджера данных"""
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager
