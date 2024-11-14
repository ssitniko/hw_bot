import random

from aiogram import types, Dispatcher
from config import bot, dp
import os




# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}\n'
                                f'Твой Telegram id - {message.from_user.id}')

    await message.answer('Привет')


async def send_mem(message: types.Message):
    photo_path = os.path.join('media', 'img.jpg')

    with open(photo_path, 'rb') as image:
        await message.answer_photo(photo=image, caption='mem')


async def game_dice(message: types.Message):
    games = ['⚽', '🎰', '🏀', '🎯', '🎳', '🎲']

    game_bot_choise = random.choice(games[0:2])
    game_user_choise = random.choice(games[3:])

    dice_roll = random.randint(1, 6)
    if dice_roll in [0, 1, 2]:
        await message.answer(game_bot_choise)
        await message.answer(f'Бот выиграл игру!: {game_bot_choise}')
    else:
        await message.answer(game_user_choise)
        await message.answer(f'Вы выиграли игру!: {game_user_choise}')


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(send_mem, commands=['mem'])
    dp.register_message_handler(game_dice, commands=['game'])
