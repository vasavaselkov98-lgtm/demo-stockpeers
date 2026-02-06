"""
Конфигурация финансовых инструментов для VV Markets Dashboard
"""

INSTRUMENT_CONFIG = {
    "periods": {
        "1d": {"name": "1 день", "description": "Дневные данные"},
        "5d": {"name": "5 дней", "description": "Недельные данные"},
        "1mo": {"name": "1 месяц", "description": "Месячные данные"},
        "3mo": {"name": "3 месяца", "description": "Квартальные данные"},
        "6mo": {"name": "6 месяцев", "description": "Полугодовые данные"},
        "1y": {"name": "1 год", "description": "Годовые данные"},
        "2y": {"name": "2 года", "description": "Двухлетние данные"},
        "5y": {"name": "5 лет", "description": "Пятилетние данные"},
        "10y": {"name": "10 лет", "description": "Десятилетние данные"},
        "max": {"name": "Максимум", "description": "Все доступные данные"}
    },
    
    "intervals": {
        "1m": {"name": "1 минута", "available_for": ["1d", "5d"]},
        "5m": {"name": "5 минут", "available_for": ["1d", "5d", "1mo"]},
        "15m": {"name": "15 минут", "available_for": ["1d", "5d", "1mo"]},
        "30m": {"name": "30 минут", "available_for": ["1d", "5d", "1mo"]},
        "1h": {"name": "1 час", "available_for": ["1d", "5d", "1mo", "3mo"]},
        "1d": {"name": "1 день", "available_for": ["all"]},
        "1wk": {"name": "1 неделя", "available_for": ["3mo", "6mo", "1y", "2y", "5y", "10y", "max"]},
        "1mo": {"name": "1 месяц", "available_for": ["1y", "2y", "5y", "10y", "max"]}
    },
    
    "chart_types": [
        {"id": "line", "name": "Линия", "icon": "📈", "description": "Линейный график"},
        {"id": "candlestick", "name": "Свечи", "icon": "🕯️", "description": "Японские свечи"},
        {"id": "ohlc", "name": "OHLC", "icon": "📊", "description": "График OHLC"},
        {"id": "area", "name": "Область", "icon": "▀", "description": "Залитый график"},
        {"id": "bar", "name": "Бары", "icon": "📊", "description": "Столбчатый график"}
    ]
}


def get_period_options():
    """Получить список периодов для selectbox"""
    return [(config["name"], key) for key, config in INSTRUMENT_CONFIG["periods"].items()]


def get_interval_options(period: str):
    """Получить доступные интервалы для периода"""
    options = []
    for interval_id, interval_config in INSTRUMENT_CONFIG["intervals"].items():
        if period in interval_config["available_for"] or "all" in interval_config["available_for"]:
            options.append((interval_config["name"], interval_id))
    return options


def get_period_name(period_key: str) -> str:
    """Получить название периода по ключу"""
    return INSTRUMENT_CONFIG["periods"].get(period_key, {}).get("name", period_key)


def get_interval_name(interval_key: str) -> str:
    """Получить название интервала по ключу"""
    return INSTRUMENT_CONFIG["intervals"].get(interval_key, {}).get("name", interval_key)
