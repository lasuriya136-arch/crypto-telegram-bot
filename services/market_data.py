import aiohttp
import pandas as pd

# Словарь для кэширования (упрощённо)
_cache = {}

async def get_ohlcv(symbol: str, vs_currency: str = "usd", days: int = 1) -> pd.DataFrame:
    """
    Получает OHLCV данные с CoinGecko.
    Возвращает DataFrame с колонками: timestamp, open, high, low, close, volume.
    """
    # Проверяем кэш (просто по ключу)
    cache_key = f"{symbol}_{vs_currency}_{days}"
    if cache_key in _cache:
        return _cache[cache_key].copy()
    
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/ohlc"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=10) as resp:
                if resp.status != 200:
                    # Попробуем прочитать текст ошибки
                    error_text = await resp.text()
                    print(f"API error {resp.status}: {error_text}")
                    return None
                data = await resp.json()
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return None
    
    if not data:
        return None
    
    # Формат: [[timestamp, open, high, low, close], ...]
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    # Добавим фиктивный объём (CoinGecko не даёт объём в этом эндпоинте)
    df["volume"] = 0  # mplfinance требует колонку volume, но мы её не используем для графика
    
    # Кэшируем
    _cache[cache_key] = df.copy()
    return df

async def get_current_price(symbol: str, vs_currency: str = "usd") -> float:
    """Получает текущую цену монеты."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": symbol,
        "vs_currencies": vs_currency
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=10) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get(symbol, {}).get(vs_currency)
        except Exception:
            return None