from aiogram import Router, types, F
from aiogram.filters import Command
from services.market_data import get_current_price
from utils.helpers import normalize_symbol

router = Router()

# Обработка команды /price
@router.message(Command("price"))
async def price_cmd(message: types.Message):
    args = message.text.split()
    raw_symbol = args[1] if len(args) > 1 else "bitcoin"
    symbol = normalize_symbol(raw_symbol)
    await send_price(message, symbol)

# Обработка всех кнопок "💰 Курс XXX"
@router.message(F.text.startswith("💰 Курс "))
async def price_button(message: types.Message):
    parts = message.text.split()
    if len(parts) >= 3:
        raw_symbol = parts[2]  # например, "BTC"
        symbol = normalize_symbol(raw_symbol)
        await send_price(message, symbol)
    else:
        await message.answer("Не удалось определить монету.")

async def send_price(message: types.Message, symbol: str):
    price = await get_current_price(symbol)
    if price is None:
        await message.answer(f"❌ Не удалось найти цену для {symbol}. Проверьте символ.")
        return
    await message.answer(f"💰 {symbol.upper()} / USD: ${price:.2f}")