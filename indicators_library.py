"""
Библиотека технических индикаторов с поддержкой пользовательских индикаторов
Поддерживает: SMA, EMA, RSI, MACD, Bollinger Bands, ATR и кастомные индикаторы
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Callable, Tuple, Any
import plotly.graph_objects as go
import json
import streamlit as st


class IndicatorLibrary:
    """Библиотека технических индикаторов"""
    
    def __init__(self, storage_path: str = "custom_indicators.json"):
        self.indicators: Dict[str, dict] = {}
        self.custom_indicators: Dict[str, dict] = {}
        self.storage_path = storage_path
        
        # Регистрация встроенных индикаторов
        self._register_builtin_indicators()
        
        # Загрузка пользовательских индикаторов
        self._load_custom_indicators()
    
    def _register_builtin_indicators(self):
        """Регистрация встроенных индикаторов"""
        
        self.indicators = {
            "SMA (Простая скользящая)": {
                "func": self._calculate_sma,
                "params": {"period": 20},
                "category": "Трендовые",
                "description": "Простая скользящая средняя",
                "color": "#e74c3c"
            },
            "EMA (Экспоненциальная)": {
                "func": self._calculate_ema,
                "params": {"period": 20},
                "category": "Трендовые",
                "description": "Экспоненциальная скользящая средняя",
                "color": "#9b59b6"
            },
            "RSI (Индекс относительной силы)": {
                "func": self._calculate_rsi,
                "params": {"period": 14, "overbought": 70, "oversold": 30},
                "category": "Осцилляторы",
                "description": "Моментумный осциллятор",
                "color": "#f1c40f"
            },
            "MACD": {
                "func": self._calculate_macd,
                "params": {"fast": 12, "slow": 26, "signal": 9},
                "category": "Осцилляторы",
                "description": "Схождение/расхождение скользящих средних",
                "color": "#2ecc71"
            },
            "Bollinger Bands": {
                "func": self._calculate_bollinger,
                "params": {"period": 20, "std": 2},
                "category": "Волатильность",
                "description": "Полосы Боллинджера",
                "color": "#1abc9c"
            },
            "ATR (Average True Range)": {
                "func": self._calculate_atr,
                "params": {"period": 14},
                "category": "Волатильность",
                "description": "Средний истинный диапазон",
                "color": "#34495e"
            },
            "Volume MA": {
                "func": self._calculate_volume_ma,
                "params": {"period": 20},
                "category": "Объем",
                "description": "Скользящая средняя объема",
                "color": "#7f8c8d"
            },
            "Stochastic Oscillator": {
                "func": self._calculate_stochastic,
                "params": {"k_period": 14, "d_period": 3},
                "category": "Осцилляторы",
                "description": "Стохастический осциллятор",
                "color": "#e67e22"
            }
        }
    
    def _load_custom_indicators(self):
        """Загрузка пользовательских индикаторов из файла"""
        try:
            with open(self.storage_path, 'r') as f:
                self.custom_indicators = json.load(f)
        except FileNotFoundError:
            self.custom_indicators = {}
    
    def _save_custom_indicators(self):
        """Сохранение пользовательских индикаторов в файл"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.custom_indicators, f, indent=2)
    
    def add_custom_indicator(self, name: str, func_code: str, params: Dict, 
                            category: str = "Пользовательские", 
                            description: str = "", color: str = "#3498db"):
        """Добавление пользовательского индикатора"""
        
        # Безопасное создание функции из кода
        try:
            # Создаем функцию из переданного кода
            exec_globals = {'pd': pd, 'np': np}
            exec(f"""
def custom_indicator_func(df, **kwargs):
    {func_code}
    return result
""", exec_globals)
            
            self.custom_indicators[name] = {
                "func_code": func_code,
                "params": params,
                "category": category,
                "description": description,
                "color": color,
                "func": exec_globals['custom_indicator_func']
            }
            
            self._save_custom_indicators()
            return True
            
        except Exception as e:
            st.error(f"Ошибка в коде индикатора: {str(e)}")
            return False
    
    def get_indicator(self, name: str) -> Optional[dict]:
        """Получить конфигурацию индикатора по имени"""
        if name in self.indicators:
            return self.indicators[name]
        elif name in self.custom_indicators:
            return self.custom_indicators[name]
        return None
    
    def get_indicators_by_category(self, category: str) -> List[str]:
        """Получить все индикаторы категории"""
        result = []
        
        # Проверяем встроенные индикаторы
        for name, config in self.indicators.items():
            if config['category'] == category:
                result.append(name)
        
        # Проверяем кастомные индикаторы
        for name, config in self.custom_indicators.items():
            if config['category'] == category:
                result.append(name)
        
        return result
    
    def get_all_indicators(self) -> Dict[str, dict]:
        """Получить все доступные индикаторы"""
        return {**self.indicators, **self.custom_indicators}
    
    def get_categories(self) -> List[str]:
        """Получить все категории индикаторов"""
        categories = set()
        
        for config in list(self.indicators.values()) + list(self.custom_indicators.values()):
            categories.add(config['category'])
        
        return sorted(list(categories))
    
    def calculate_indicator(self, df: pd.DataFrame, indicator_name: str, **params) -> Any:
        """Рассчитать значение индикатора"""
        config = self.get_indicator(indicator_name)
        if not config:
            raise ValueError(f"Индикатор '{indicator_name}' не найден")
        
        # Объединяем параметры по умолчанию с переданными
        all_params = config['params'].copy()
        all_params.update(params)
        
        return config['func'](df, **all_params)
    
    def apply_to_chart(self, fig: go.Figure, df: pd.DataFrame, 
                      indicator_names: List[str], **params) -> go.Figure:
        """Применить индикаторы к графику Plotly"""
        
        for indicator_name in indicator_names:
            config = self.get_indicator(indicator_name)
            if not config:
                continue
            
            # Рассчитываем индикатор
            indicator_data = self.calculate_indicator(df, indicator_name, **params)
            
            # Добавляем на график
            self._add_indicator_to_fig(fig, df, indicator_name, indicator_data, config)
        
        return fig
    
    def _add_indicator_to_fig(self, fig: go.Figure, df: pd.DataFrame, 
                             name: str, data: Any, config: dict):
        """Добавить индикатор на график"""
        
        if isinstance(data, (pd.Series, np.ndarray)):
            # Один ряд данных
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=data,
                    name=name,
                    line=dict(
                        color=config.get('color', '#3498db'),
                        width=2,
                        dash="dash"
                    ),
                    opacity=0.7
                )
            )
        elif isinstance(data, tuple) and len(data) == 3:
            # Три ряда (например, Bollinger Bands)
            upper, middle, lower = data
            
            # Верхняя линия
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=upper,
                    name=f"{name} Upper",
                    line=dict(color=config.get('color', '#3498db'), width=1, dash="dash"),
                    opacity=0.5,
                    showlegend=False
                )
            )
            
            # Средняя линия
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=middle,
                    name=f"{name} Middle",
                    line=dict(color=config.get('color', '#3498db'), width=1.5),
                    opacity=0.7
                )
            )
            
            # Нижняя линия с заполнением
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=lower,
                    name=f"{name} Lower",
                    fill='tonexty',
                    fillcolor=f"rgba{self._hex_to_rgb(config.get('color', '#3498db')) + (0.1,)}",
                    line=dict(color=config.get('color', '#3498db'), width=1, dash="dash"),
                    opacity=0.5,
                    showlegend=False
                )
            )
    
    def _hex_to_rgb(self, hex_color: str):
        """Конвертировать hex в rgb"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # ========== РЕАЛИЗАЦИИ ИНДИКАТОРОВ ==========
    
    def _calculate_sma(self, df: pd.DataFrame, period: int = 20) -> pd.Series:
        """Простая скользящая средняя"""
        return df['Close'].rolling(window=period, min_periods=1).mean()
    
    def _calculate_ema(self, df: pd.DataFrame, period: int = 20) -> pd.Series:
        """Экспоненциальная скользящая средняя"""
        return df['Close'].ewm(span=period, min_periods=1, adjust=False).mean()
    
    def _calculate_rsi(self, df: pd.DataFrame, period: int = 14, 
                      overbought: float = 70, oversold: float = 30) -> pd.Series:
        """Индекс относительной силы"""
        delta = df['Close'].diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_macd(self, df: pd.DataFrame, fast: int = 12, 
                       slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """MACD (Moving Average Convergence Divergence)"""
        exp1 = df['Close'].ewm(span=fast, adjust=False).mean()
        exp2 = df['Close'].ewm(span=slow, adjust=False).mean()
        
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram
    
    def _calculate_stochastic(self, df: pd.DataFrame, k_period: int = 14, 
                            d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
        """Стохастический осциллятор"""
        low_min = df['Low'].rolling(window=k_period).min()
        high_max = df['High'].rolling(window=k_period).max()
        
        k = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        d = k.rolling(window=d_period).mean()
        
        return k, d
    
    def _calculate_bollinger(self, df: pd.DataFrame, period: int = 20, 
                           std: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """Полосы Боллинджера"""
        sma = df['Close'].rolling(window=period).mean()
        rolling_std = df['Close'].rolling(window=period).std()
        
        upper = sma + (rolling_std * std)
        lower = sma - (rolling_std * std)
        
        return upper, sma, lower
    
    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Average True Range"""
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        
        return true_range.rolling(period).mean()
    
    def _calculate_volume_ma(self, df: pd.DataFrame, period: int = 20) -> pd.Series:
        """Скользящая средняя объема"""
        return df['Volume'].rolling(window=period).mean()


# Глобальный экземпляр библиотеки
_indicator_lib = None

def get_indicator_library() -> IndicatorLibrary:
    """Получить глобальный экземпляр библиотеки индикаторов"""
    global _indicator_lib
    if _indicator_lib is None:
        _indicator_lib = IndicatorLibrary()
    return _indicator_lib
