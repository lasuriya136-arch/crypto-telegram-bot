import pandas as pd

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> float:
    """Расчёт RSI (последнее значение)."""
    if len(df) < period:
        return 50.0  # недостаточно данных
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    if loss.iloc[-1] == 0:
        return 100.0
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def calculate_ema(df: pd.DataFrame, period: int = 20) -> float:
    """Расчёт EMA (последнее значение)."""
    if len(df) < period:
        return df["close"].iloc[-1]  # возвращаем цену, если данных мало
    return df["close"].ewm(span=period, adjust=False).mean().iloc[-1]

def generate_signal(df: pd.DataFrame) -> dict:
    """
    Генерирует сигнал на основе RSI (14) и EMA (20).
    Возвращает словарь с action и reason.
    """
    if df.empty or len(df) < 20:
        return None
    
    rsi = calculate_rsi(df)
    ema = calculate_ema(df)
    current_price = df["close"].iloc[-1]
    
    if rsi < 30 and current_price > ema:
        return {
            "action": "BUY",
            "reason": f"RSI={rsi:.1f} (<30) и цена выше EMA20"
        }
    elif rsi > 70 and current_price < ema:
        return {
            "action": "SELL",
            "reason": f"RSI={rsi:.1f} (>70) и цена ниже EMA20"
        }
    else:
        return {
            "action": "HOLD",
            "reason": f"RSI={rsi:.1f}, нет явного сигнала"
        }