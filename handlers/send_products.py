from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from db import db_main

from aiogram.dispatcher.filters.state import State, StatesGroup



class ProductState(StatesGroup):
    enter_product_name = State()


async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_all = types.InlineKeyboardButton('Вывести все товары', callback_data='all')
    button_one = types.InlineKeyboardButton('Вывести по одному', callback_data='one')
    keyboard.add(button_all, button_one)

    await message.answer('Выберите как отправить товары:', reply_markup=keyboard)


async def send_all_products(callback_query: types.CallbackQuery):
    products = db_main.fetch_all_products()
    if products:
        for product in products:
            caption = (f"Заполненный товар: \n"
                       f"Название - {product['name_product']}\n"
                       f"Артикул - {product['product_id']}\n"
                       f"Размер - {product['size']}\n"
                       f"Цена - {product['price']}\n"
                       f"Информация о товаре - {product['info_product']}\n"
                       f"Категория - {product['category']}\n")
            await callback_query.message.answer_photo(
                photo=product['photo'],
                caption=caption
            )
    else:
        await callback_query.message.answer(text='В базе товаров нет!')


async def send_one_product(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Введите название товара: ')
    await ProductState.enter_product_name.set()


async def handle_product_name(message: types.Message, state: FSMContext):
    name_product = message.text.strip()
    product = db_main.fetch_one_product(name_product)
    if product:
        caption = (f"Заполненный товар: \n"
                   f"Название - {product['name_product']}\n"
                   f"Артикул - {product['product_id']}\n"
                   f"Размер - {product['size']}\n"
                   f"Цена - {product['price']}\n"
                   f"Информация о товаре - {product['info_product']}\n"
                   f"Категория - {product['category']}\n")

        # delete_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        # delete_button = types.InlineKeyboardButton('Удалить', callback_data=f'delete_{product["product_id"]}')
        # delete_keyboard.add(delete_button)

        await message.answer_photo(
            photo=product['photo'],
            caption=caption,
            # reply_markup = delete_keyboard
        )
    else:
        await message.answer(text='Такого товара в базе нет!')

    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands='send_products')
    dp.register_callback_query_handler(send_all_products, Text(equals='all'))
    dp.register_callback_query_handler(send_one_product, Text(equals='one'))
    dp.register_message_handler(handle_product_name, state=ProductState.enter_product_name)
