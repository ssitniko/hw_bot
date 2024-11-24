from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel, size_list, confirm_list
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from db import db_main



class fsm_store(StatesGroup):
    name_product = State()
    size = State()
    collection = State()
    category = State()
    product_id = State()
    info_product = State()
    price = State()
    photo = State()

async def start_fsm(message: types.Message):
    await message.answer('Введите название товара: ')
    await fsm_store.name_product.set()

async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text


    await fsm_store.next()
    await message.answer('Выберите размер:', reply_markup=size_list)


async def process_size_select(callback_query: CallbackQuery, state: FSMContext):
    size = callback_query.data
    async with state.proxy() as data:
        data['size'] = size
    await callback_query.answer()

    await fsm_store.next()
    await callback_query.message.answer('Введите коллекцию:')


async def collection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['collection'] = message.text

    await fsm_store.next()
    await message.answer('Введите категорию товара:')


async def load_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await fsm_store.next()
    await message.answer('Введите артикул товара:')


async def product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit():
            data['product_id'] = int(message.text)
            await fsm_store.next()
            await message.answer('Введите информацию о товаре:')
        else:
            await message.answer('Введите артикул только цифрами')
            await fsm_store.product_id.set()

async def info_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text

    await fsm_store.next()
    await message.answer('Введите стоимость товара:')

async def load_product_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await fsm_store.next()
    await message.answer('Отправьте фото')

async def load_product_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    # await state.finish()
    await message.answer_photo(photo=data['photo'],
                               caption= f'Название товара - {data["name_product"]}\n'
                                        f'Размер - {data["size"]}\n'
                                        f'Коллекция - {data["collection"]}\n'
                                        f'Категория - {data["category"]}\n'
                                        f'Артикул - {data["product_id"]}\n'
                                        f'Информация - {data["info_product"]}\n'
                                        f'Цена - {data["price"]}\n')


    await message.answer('Верные ли данные?:', reply_markup=confirm_list)

# async def process_confirm_select(callback_query: CallbackQuery, state: FSMContext):
#     if callback_query.data == 'Да':
#         await callback_query.message.answer('Сохранено в базу')
#         await state.finish()
#     elif callback_query.data == 'Нет':
#         await state.finish()


async def submit(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'Да':
        await callback_query.message.answer('Отлично, товар в базе!')

        async with state.proxy() as data:
            await db_main.sql_insert_store(
                name_product=data['name_product'],
                size=data['size'],
                collection=data['collection'],
                category=data['category'],
                product_id=data['product_id'],
                info_product=data['info_product'],
                price=data['price'],
                photo=data['photo']
            )

            await db_main.sql_insert_product_details(
                product_id=data['product_id'],
                category=data['category'],
                info_product=data['info_product']
            )

            await db_main.sql_insert_collection_products(
                product_id=data['product_id'],
                collection=data['collection']
            )

    elif callback_query.data == 'Нет':
        await callback_query.message.answer('Отменено!')

    else:
        await callback_query.answer('Введите Да или Нет')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)



def reg_handler_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_fsm, commands=['store'])
    dp.register_message_handler(load_name_product, state=fsm_store.name_product)
    dp.register_callback_query_handler(process_size_select, state=fsm_store.size)
    dp.register_message_handler(collection, state=fsm_store.collection)
    dp.register_message_handler(load_product_category, state=fsm_store.category)
    dp.register_message_handler(product_id, state=fsm_store.product_id)
    dp.register_message_handler(info_product, state=fsm_store.info_product)
    dp.register_message_handler(load_product_price, state=fsm_store.price)
    dp.register_message_handler(load_product_photo, state=fsm_store.photo, content_types=['photo'])
    dp.register_callback_query_handler(submit, Text(equals='Да'), state=fsm_store.photo)
    dp.register_callback_query_handler(submit, Text(equals='Нет'), state=fsm_store.photo)

    # dp.register_callback_query_handler(process_confirm_select, Text(equals='Да'), state=fsm_store.photo)
    # dp.register_callback_query_handler(process_confirm_select, Text(equals='Нет'), state=fsm_store.photo)






