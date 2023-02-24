import handlers
from aiogram import executor
from loader import dp
from utils.set_bot_commands import set_default_commands
from data.config import *
from utils.middlware import *

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

#Разработчики: https://t.me/weaseldev @weaseldev

if __name__ == '__main__':
    print('гуд')
    dp.middleware.setup(OffCallback())
    dp.middleware.setup(OffMessage())
    dp.middleware.setup(SearchBanUserCallback())
    dp.middleware.setup(Ads())
    dp.middleware.setup(SubsribeOnChannelMessage())
    dp.middleware.setup(SubsribeOnChannelCallback())
    dp.middleware.setup(ThrottlingMiddleware())
    
    executor.start_polling(dp, on_startup=on_startup)