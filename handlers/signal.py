from aiogram import Router, types, F
from aiogram.filters import Command
from services.market_data import get_ohlcv
from services.indicators import generate_signal
from utils.helpers import normalize_symbol

router = Router()

@router.message(Command("signal"))
async def signal_cmd(message: types.Message):
    args = message.text.split()
    raw_symbol = args[1] if len(args) > 1 else "bitcoin"
    symbol = normalize_symbol(raw_symbol)
    await send_signal(message, symbol)

@router.message(F.text.startswith("📈 Сигнал "))
async def signal_button(message: types.Message):
    parts = message.text.split()
    if len(parts) >= 3:
        raw_symbol = parts[2]
        symbol = normalize_symbol(raw_symbol)
        await send_signal(message, symbol)
    else:
        await message.answer("Неверный формат.")

async def send_signal(message: types.Message, symbol: str):
    await message.answer("⏳ Анализирую данные...")
    df = await get_ohlcv(symbol, days=7)
    if df is None or df.empty:
        await message.answer(f"❌ Не удалось получить данные для {symbol}.")
        return
    signal = generate_signal(df)
    if signal is None:
        await message.answer("❌ Недостаточно данных для генерации сигнала.")
        return
    action = signal["action"]
    reason = signal["reason"]
    emoji = "🟢" if action == "BUY" else "🔴" if action == "SELL" else "🟡"
    text = (
        f"{emoji} Сигнал для **{symbol.upper()}**\n"
        f"Действие: **{action}**\n"
        f"Обоснование: {reason}"
    )
    await message.answer(text, parse_mode="Markdown")