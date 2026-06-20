from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.market_data import get_ohlcv
from utils.chart_builder import build_chart
from utils.helpers import normalize_symbol

router = Router()

def get_timeframe_keyboard(symbol: str, current_tf: str):
    tf_list = ["1h", "4h", "24h", "7d"]
    buttons = []
    for tf in tf_list:
        label = f"✅ {tf}" if tf == current_tf else tf
        buttons.append(InlineKeyboardButton(
            text=label,
            callback_data=f"chart_{symbol}_{tf}"
        ))
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i+2] for i in range(0, len(buttons), 2)])
    return keyboard

@router.message(Command("chart"))
async def chart_cmd(message: types.Message):
    args = message.text.split()
    raw_symbol = args[1] if len(args) > 1 else "bitcoin"
    symbol = normalize_symbol(raw_symbol)
    
    days_map = {"1h": 1, "4h": 1, "24h": 1, "7d": 7}
    timeframe = args[2] if len(args) > 2 else "24h"
    days = days_map.get(timeframe, 1)
    
    await message.answer("⏳ Загружаю данные и строю график...")
    df = await get_ohlcv(symbol, days=days)
    if df is None or df.empty:
        await message.answer(f"❌ Не удалось получить данные для {symbol}.")
        return
    img_bytes = build_chart(df, f"{symbol.upper()} {timeframe}")
    if img_bytes is None:
        await message.answer("❌ Ошибка при построении графика.")
        return
    await message.answer_photo(
        photo=types.BufferedInputFile(img_bytes, filename="chart.png"),
        caption=f"📊 {symbol.upper()} — {timeframe}",
        reply_markup=get_timeframe_keyboard(symbol, timeframe)
    )

# Обработка кнопок "📊 График XXX 1h" из Reply-клавиатуры
@router.message(F.text.startswith("📊 График "))
async def chart_button(message: types.Message):
    parts = message.text.split()
    if len(parts) >= 4:
        raw_symbol = parts[2]
        symbol = normalize_symbol(raw_symbol)
        timeframe = parts[3].lower()
        days_map = {"1h": 1, "4h": 1, "24h": 1, "7d": 7}
        days = days_map.get(timeframe, 1)
        await message.answer("⏳ Загружаю данные и строю график...")
        df = await get_ohlcv(symbol, days=days)
        if df is None or df.empty:
            await message.answer(f"❌ Не удалось получить данные для {symbol}.")
            return
        img_bytes = build_chart(df, f"{symbol.upper()} {timeframe}")
        if img_bytes is None:
            await message.answer("❌ Ошибка при построении графика.")
            return
        await message.answer_photo(
            photo=types.BufferedInputFile(img_bytes, filename="chart.png"),
            caption=f"📊 {symbol.upper()} — {timeframe}",
            reply_markup=get_timeframe_keyboard(symbol, timeframe)
        )
    else:
        await message.answer("Неверный формат кнопки.")

# Обработка нажатий на инлайн-кнопки (смена таймфрейма)
@router.callback_query(lambda c: c.data.startswith("chart_"))
async def process_timeframe_callback(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.answer("Ошибка", show_alert=True)
        return
    symbol = parts[1]
    timeframe = parts[2]
    days_map = {"1h": 1, "4h": 1, "24h": 1, "7d": 7}
    days = days_map.get(timeframe, 1)
    
    await callback.message.delete()
    await callback.answer(f"Загружаю график {symbol} {timeframe}...")
    
    df = await get_ohlcv(symbol, days=days)
    if df is None or df.empty:
        await callback.message.answer(f"❌ Не удалось получить данные для {symbol}.")
        return
    img_bytes = build_chart(df, f"{symbol.upper()} {timeframe}")
    if img_bytes is None:
        await callback.message.answer("❌ Ошибка при построении графика.")
        return
    await callback.message.answer_photo(
        photo=types.BufferedInputFile(img_bytes, filename="chart.png"),
        caption=f"📊 {symbol.upper()} — {timeframe}",
        reply_markup=get_timeframe_keyboard(symbol, timeframe)
    )   