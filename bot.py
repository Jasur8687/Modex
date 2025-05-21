import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, FSInputFile
from aiogram.filters import Command
from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()
client = TelegramClient("bot_session", API_ID, API_HASH)

logging.basicConfig(level=logging.INFO)

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def start_telethon():
    await client.start(password=PASSWORD)
    print("✅ Telethon авторизован!")

@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 Инструкция", url="https://t.me/modex_vzlom")],
        [InlineKeyboardButton(text="✅ Я подписался", callback_data="subscribed")]
    ])
    await message.answer(
        "Добро пожаловать в MODEX BOT! Перед началом подпишись на канал и прочитай инструкцию:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "subscribed")
async def subscribed_handler(callback_query: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Пройти регистрацию", url="https://1wprde.com/?open=register&p=vayp")]
    ])
    await callback_query.message.answer(
        "Отлично! Теперь пройди регистрацию на платформе, затем отправь сюда свой 9-значный ID:",
        reply_markup=keyboard
    )
    await callback_query.answer()

@dp.message()
async def check_id(message: Message):
    user_id = message.text.strip()
    if not user_id.isdigit()  or not (6 <= len(user_id) <= 12):
         await message.answer("⚠ Введите корректный 9-значный ID!")
         return


    try:
        async for msg in client.iter_messages(CHANNEL_ID, limit=50):
            if msg.text and user_id in msg.text:
                cover = FSInputFile("cover.jpg")
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🚀 ОТКРЫТЬ", url="https://t.me/skript1win_bot/skriptbot")]
                ])
                await message.answer("✅ Ваш ID найден! Доступ разрешён.")
                await message.answer_photo(photo=cover, caption="Открыть Программу:", reply_markup=keyboard)
                return

        await message.answer("⛔ Ваш ID не найден. Пожалуйста, пройди регистрацию строго по инструкции с канала.")

    except Exception as e:
        logging.error(f"Ошибка при проверке ID: {e}")
        await message.answer("❌ Ошибка при доступе к каналу. Проверь, что бот админ.")

async def main():
    await start_telethon()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
