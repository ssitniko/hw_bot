from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel, size_list, confirm_list
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery

class fsm_store(StatesGroup):
    product_name = State()
    size = State()
    category = State()
    price = State()
    photo = State()

async def start_fsm(message: types.Message):
    await message.answer('Введите название товара: ')
    await fsm_store.product_name.set()

async def load_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text


    await fsm_store.next()
    await message.answer('Выберите размер:', reply_markup=size_list)


async def process_size_select(callback_query: CallbackQuery, state: FSMContext):
    size = callback_query.data
    async with state.proxy() as data:
        data['size'] = size
    await callback_query.answer()

    await fsm_store.next()
    await callback_query.message.answer('Введите категорию товара:')

async def load_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

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
    await message.answer_photo(photo=data['photo'], caption= f'Название товара - {data["product_name"]}\n'
                               f'Размер - {data["size"]}\n' f'Category - {data["category"]}\n' f'Price - {data["price"]}\n')

    # await fsm_store.next()
    await message.answer('Верные ли данные?:', reply_markup=confirm_list)

async def process_confirm_select(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'Да':
        await callback_query.message.answer('Сохранено в базу')
        await state.finish()
    elif callback_query.data == 'Нет':
        await state.finish()



async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    kb_remove = ReplyKeyboardRemove()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено', reply_markup=kb_remove)



def reg_handler_fsm_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_fsm, commands=['store'])
    dp.register_message_handler(load_product_name, state=fsm_store.product_name)
    dp.register_callback_query_handler(process_size_select, state=fsm_store.size)
    dp.register_message_handler(load_product_category, state=fsm_store.category)
    dp.register_message_handler(load_product_price, state=fsm_store.price)
    dp.register_message_handler(load_product_photo, state=fsm_store.photo, content_types=['photo'])
    dp.register_callback_query_handler(process_confirm_select, Text(equals='Да'), state=fsm_store.photo)
    dp.register_callback_query_handler(process_confirm_select, Text(equals='Нет'), state=fsm_store.photo)






