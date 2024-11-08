from aiogram import Bot, Dispatcher
from decouple import config
import os

token = config('TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)