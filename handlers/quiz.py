from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot
import os

async def quiz_1(message: types.Message):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Далее', callback_data='quiz_2')

    keyboard.add(button)

    question = 'Where are you from ?'

    options = ['Bishkek', 'Moscow', 'Tokyo', 'Tashkent']

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=options,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation='Саткын!!!!',
        open_period=60,
        reply_markup=keyboard
    )


async def quiz_2(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Следующее', callback_data='quiz_3')

    keyboard.add(button)

    question = 'Выбери страну'

    options = ['Kyrgyzstan', 'Russia', 'Uzbekistan', 'China', 'Japan', 'USA']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=options,
        is_anonymous=True,
        type='quiz',
        correct_option_id=0,
        explanation='Эмигрант',
        open_period=60,
        reply_markup=keyboard
    )


async def quiz_3(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)

    button = InlineKeyboardButton('Следующее', callback_data='quiz_3')

    keyboard.add(button)


    photo_path = os.path.join('media', 'duckbill.jpg')
    await bot.send_photo(chat_id=call.from_user.id, photo=open(photo_path, 'rb'), caption="Вот изображение для вопроса.")


    question = 'Утконос это? (выбери правильный ответ)'

    options = ['пресноводное', 'птица', 'млекопитающее']

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=options,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation='???',
        open_period=60,
        reply_markup=keyboard
    )



def register_handler_quiz(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, text='quiz_2')
    dp.register_callback_query_handler(quiz_3, text='quiz_3')
