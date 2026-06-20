import io
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def build_chart(df: pd.DataFrame, title: str) -> bytes:
    """
    Строит свечной график с EMA (20) и возвращает байты PNG.
    """
    if df.empty or len(df) < 5:
        return None
    
    # Копируем, чтобы не изменять оригинал
    data = df.copy()
    # Добавляем EMA20
    data["EMA20"] = data["close"].ewm(span=20, adjust=False).mean()
    
    # Дополнительные графики
    apds = [mpf.make_addplot(data["EMA20"], color="blue", width=1)]
    
    # Строим график
    fig, axes = mpf.plot(
        data,
        type="candle",
        style="charles",
        volume=False,  # отключаем объём, т.к. у нас нет реальных данных
        addplot=apds,
        title=title,
        ylabel="Price (USD)",
        figsize=(10, 6),
        returnfig=True
    )
    
    # Сохраняем в буфер
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)  # закрываем, чтобы не плодить окна
    buf.seek(0)
    return buf.getvalue()