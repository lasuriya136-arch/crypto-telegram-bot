from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="💰 Курс BTC"), KeyboardButton(text="💰 Курс ETH")],
        [KeyboardButton(text="💰 Курс SOL"), KeyboardButton(text="💰 Курс DOGE")],
        [KeyboardButton(text="💰 Курс ADA"), KeyboardButton(text="💰 Курс DOT")],
        [KeyboardButton(text="📊 График BTC 1h"), KeyboardButton(text="📈 Сигнал BTC")],
        [KeyboardButton(text="📊 График ETH 1h"), KeyboardButton(text="📈 Сигнал ETH")],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    text = (
        "🤖 Привет! Я крипто-бот с графиками и сигналами.\n\n"
        "Используй команды или нажимай на кнопки ниже 👇\n"
        "/price <символ> — текущая цена\n"
        "/chart <символ> <таймфрейм> — график\n"
        "/signal <символ> — сигнал"
    )
    await message.answer(text, reply_markup=get_main_keyboard())