import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.enums import ParseMode

# Используем токен из переменных окружения Railway
TOKEN = os.getenv("7765691064:AAGpZY2y9IhuJJTX5crdhaFdwOapvAyrH3Y")

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Категории товаров
categories = {
    "iPhone": ["Дисплей", "Аккумулятор", "Стекло"],
    "Apple Watch": ["Дисплей", "Корпус"],
    "iPad": ["Аккумулятор", "Сенсор"]
}

# Товары
products = {
    "iPhone / дисплей": [
        {"name": "Дисплей iPhone 16 Pro Max", "price": "30 000 руб.", "desc": "Оригинальный дисплей", "photo": "https://via.placeholder.com/150"},
        {"name": "Дисплей iPhone 13", "price": "15 000 руб.", "desc": "Дисплей высокого качества", "photo": "https://via.placeholder.com/150"}
    ]
}

# Главное меню
def main_menu():
    markup = InlineKeyboardMarkup()
    for category in categories.keys():
        markup.add(InlineKeyboardButton(category, callback_data=f"cat_{category}"))
    return markup

# Подкатегории
def subcategory_menu(category):
    markup = InlineKeyboardMarkup()
    for sub in categories.get(category, []):
        markup.add(InlineKeyboardButton(sub, callback_data=f"sub_{category}_{sub}"))
    return markup

# Команда /start
@dp.message_handler(Command("start"))
async def start_command(message: Message):
    await message.answer("Выберите категорию:", reply_markup=main_menu())

# Выбор подкатегории
@dp.callback_query_handler(lambda c: c.data.startswith("cat_"))
async def show_subcategories(callback_query: types.CallbackQuery):
    category = callback_query.data.split("_")[1]
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали {category}. Выберите подкатегорию:", reply_markup=subcategory_menu(category))

# Показ товаров
@dp.callback_query_handler(lambda c: c.data.startswith("sub_"))
async def show_products(callback_query: types.CallbackQuery):
    , category, subcategory = callback_query.data.split("")
    key = f"{category} / {subcategory}"
    
    if key in products:
        for item in products[key]:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🛒 Заказать", callback_data=f"order_{item['name']}"))
            await bot.send_photo(callback_query.from_user.id, item["photo"],
                                 caption=f"📌 {item['name']}\n💰 Цена: {item['price']}\n📖 {item['desc']}", reply_markup=markup)
    else:
        await bot.send_message(callback_query.from_user.id, "❌ В данной подкатегории пока нет товаров.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if _name_ == "_main_":
    asyncio.run(main())
