import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from aiogram.dispatcher.router import Router
from dotenv import load_dotenv

# Загрузка токена из .env файла
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()


# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
        ],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)


# Обработчик кнопок "Привет" и "Пока"
@router.message(lambda msg: msg.text in ["Привет", "Пока"])
async def greeting_handler(message: types.Message):
    if message.text == "Привет":
        response = f"Привет, {message.from_user.full_name}!"
    elif message.text == "Пока":
        response = f"До свидания, {message.from_user.full_name}!"
    await message.answer(response)


# Обработчик команды /links
@router.message(Command("links"))
async def links_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://dzen.ru/news?utm_referrer=dzen.ru")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru/home?from=tableau_yabro")],
        [InlineKeyboardButton(text="Видео", url="https://dzen.ru/video")],
    ])
    await message.answer("Выберите ссылку:", reply_markup=keyboard)


# Обработчик команды /dynamic
@router.message(Command("dynamic"))
async def dynamic_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Динамическое меню:", reply_markup=keyboard)


# Обработчик нажатия кнопки "Показать больше"
@router.callback_query(lambda cb: cb.data == "show_more")
async def show_more_callback(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")],
    ])
    await callback_query.message.edit_text("Выберите опцию:", reply_markup=keyboard)


# Обработчик нажатий "Опция 1" и "Опция 2"
@router.callback_query(lambda cb: cb.data in ["option_1", "option_2"])
async def option_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "option_1":
        response = "Вы выбрали Опцию 1"
    elif callback_query.data == "option_2":
        response = "Вы выбрали Опцию 2"
    await callback_query.message.answer(response)


# Регистрация обработчиков
dp.include_router(router)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
