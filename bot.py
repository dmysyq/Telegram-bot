import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import pyperclip
from main import get_parsed_products

# Загрузка переменных окружения из файла .env
load_dotenv()

# Инициализация логгера
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher()


async def send_product(channel_id, products_to_send):
    message_text = (
        f"{products_to_send.title}\n\n"

        f"{products_to_send.price} " f"({products_to_send.discount}%)\n"
        f"Цена без скидки: {products_to_send.old_price}\n\n"
        
        f"{products_to_send.link}\n"
    )

    await bot.send_message(channel_id, message_text)

'''
def get_translations(user_id):
    # Путь к файлу локализации
    localization_path = f"localization/translations_{user_id}.json"
    
    # Загрузка переводов из файла
    with open(localization_path, "r", encoding="utf-8") as file:
        translations = json.load(file)
    
    return translations
'''
# Обработка команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Каналы"), types.KeyboardButton(text="Цены")],
        [types.KeyboardButton(text="Продлить подписку"), types.KeyboardButton(text="Моя подписка"), types.KeyboardButton(text="Сменить язык")],
        [types.KeyboardButton(text="Показать мой ID"), types.KeyboardButton(text="Рекомендовать")],  # Добавлено "Скидки"
    ]
    
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Доступные команды", reply_markup=keyboard)


@dp.message(lambda message: message.text == "Цены")
async def shops_handler(message: types.Message):
    kb_shops = [
        [types.KeyboardButton(text="shop.kz"), types.KeyboardButton(text="sulpak.kz"), types.KeyboardButton(text="dns-shop.kz")],
        [types.KeyboardButton(text='/start')]
    ]

    keyboard_shops = types.ReplyKeyboardMarkup(keyboard=kb_shops, resize_keyboard=True)
    await message.answer("Выберите желаемый магазин", reply_markup=keyboard_shops)


@dp.message(lambda message: message.text == "shop.kz")
async def shop_kz_handler(message: types.Message):
    kb_shop_kz = [
        [types.KeyboardButton(text="Смартфоны shop.kz"), types.KeyboardButton(text="Видеокарты shop.kz"), types.KeyboardButton(text="Ноутбуки shop.kz")],
        [types.KeyboardButton(text='/start')]
    ]

    keyboard_shop_kz = types.ReplyKeyboardMarkup(keyboard=kb_shop_kz, resize_keyboard=True)
    await message.answer("Выберите категорию в shop.kz", reply_markup=keyboard_shop_kz)


@dp.message(lambda message: message.text == "Смартфоны shop.kz")
async def smartphones_handler(message: types.Message):
    category = 'smartphones_shopkz'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)


@dp.message(lambda message: message.text == "Видеокарты shop.kz")
async def video_cards_handler(message: types.Message):
    category = 'video_cards_shopkz'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)


@dp.message(lambda message: message.text == "Ноутбуки shop.kz")
async def laptops_handler(message: types.Message):
    category = 'laptops_shopkz'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)


@dp.message(lambda message: message.text == "sulpak.kz")
async def sulpak_kz_handler(message: types.Message):
    kb_sulpak_kz = [
        [types.KeyboardButton(text="Смартфоны sulpak.kz"), types.KeyboardButton(text="Видеокарты sulpak.kz"), types.KeyboardButton(text="Ноутбуки sulpak.kz")],
        [types.KeyboardButton(text='/start')]
    ]

    keyboard_sulpak_kz = types.ReplyKeyboardMarkup(keyboard=kb_sulpak_kz, resize_keyboard=True)
    await message.answer("Выберите категорию в sulpak.kz", reply_markup=keyboard_sulpak_kz)


@dp.message(lambda message: message.text == "Смартфоны sulpak.kz")
async def smartphones_sulpak_handler(message: types.Message):
    category = 'smartphones_sulpakkz'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)


@dp.message(lambda message: message.text == "Видеокарты sulpak.kz")
async def video_cards_sulpak_handler(message: types.Message):
    category = 'video_cards_sulpakkz'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)


@dp.message(lambda message: message.text == "Ноутбуки sulpak.kz")
async def laptops_sulpak_handler(message: types.Message):
    category = 'laptops_sulpakkz'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)

@dp.message(lambda message: message.text == "dns-shop.kz")
async def dns_shop_handler(message: types.Message):
    kb_dns_shop = [
        [types.KeyboardButton(text="Смартфоны DNS"), types.KeyboardButton(text="Видеокарты DNS"), types.KeyboardButton(text="Ноутбуки DNS")],
        [types.KeyboardButton(text='/start')]
    ]

    keyboard_dns_shop = types.ReplyKeyboardMarkup(keyboard=kb_dns_shop, resize_keyboard=True)
    await message.answer("Выберите категорию в dns-shop.kz", reply_markup=keyboard_dns_shop)

@dp.message(lambda message: message.text == "Смартфоны DNS")
async def smartphones_dns_handler(message: types.Message):
    category = 'smartphones_dns'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)

@dp.message(lambda message: message.text == "Видеокарты DNS")
async def video_cards_dns_handler(message: types.Message):
    category = 'video_cards_dns'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)

@dp.message(lambda message: message.text == "Ноутбуки DNS")
async def laptops_dns_handler(message: types.Message):
    category = 'laptops_dns'
    channel_id = message.chat.id
    parsed_products = get_parsed_products(category, start_page=1, end_page=10)

    for product in parsed_products:
        await send_product(channel_id, product)

# Обработка команды "Каналы"
@dp.message(lambda message: message.text == "Каналы")
async def show_channels(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Канал с рассылкой", url="обновится позже")) # https://t.me/+_ooSjqH70_JiMTk6
    await message.answer("Канал с рассылкой", reply_markup=builder.as_markup())

# Обработка команды "Показать мой ID"
@dp.message(lambda message: message.text == "Показать мой ID")
async def show_user_id(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"Ваш ID: {user_id}")

# Обработка команды "Продлить подписку"
@dp.message(lambda message: message.text == "Продлить подписку")
async def extend_subscription(message: types.Message):
    await message.answer("Извините, функция 'Продлить подписку' скоро станет доступной.")

# Обработка команды "Моя подписка"
@dp.message(lambda message: message.text == "Моя подписка")
async def my_subscription(message: types.Message):
    await message.answer("Извините, функция 'Моя подписка' скоро станет доступной.")

# Кнопка "Рекомендовать"
@dp.message(lambda message: message.text == "Рекомендовать")
async def recommend_bot(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Рекомендовать бота", callback_data="copy_recommendation"))

    await message.answer(
        "Рекомендую вам использовать этого бота! 👍\n\n"
        "Для копирования текста, нажмите кнопку ниже и скопируйте текст вручную.",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(lambda c: c.data == "copy_recommendation")
async def copy_recommendation(callback_query: types.CallbackQuery):
    recommendation_text = "Рекомендую вам использовать этого бота! 👍\n\n https://t.me/SkidkiKZ_Bot"
    await callback_query.answer(f"Текст скопирован: {recommendation_text}. Теперь вы можете вставить его вручную.")
    pyperclip.copy(recommendation_text)

# Обработка нажатия на кнопку "Сменить язык"
'''
@dp.message(lambda message: message.text == get_translations(message.from_user.id)["change_language"])
async def change_language(message: types.Message):
    translations = get_translations(message.from_user.id)
    await message.answer(translations["choose_language"])
'''
# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
