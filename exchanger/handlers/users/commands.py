from aiogram import types
from aiogram.types import *
from data.config import *
from loader import dp, bot
from keyboards import inline_keyboards as ikb
from utils.database import *
from utils.middlware import *


@dp.message_handler(commands='start')
async def start(message: types.Message):
    
    id = message.from_id
    name_user = message.from_user.full_name
    username = message.from_user.username

    with DB() as db:
        db.add_user(id, name_user, username)

    await message.answer('Добро пожаловать в обменник!', reply_markup=ikb.main_menu_inline)
