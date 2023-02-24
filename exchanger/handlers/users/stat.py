from aiogram import types
from aiogram.types import *
from data.config import *
from loader import dp, bot
from keyboards import inline_keyboards as ikb
from utils.database import *
from states.state import *




@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='statsric')
async def stat_func(call: types.CallbackQuery):

    with DB() as db:
        req = db.give_stat_admin()

    valute = []

    for valute_name in req:

        valute.append(valute_name[1])

    valute_list = list(set(valute))

    text = 'Статистика обменов за все время:\n\n'

    for name in valute_list:
        n = 0
        for in_list in req:
            if name == in_list[1]:
                n += float(in_list[2])
            else:
                pass
        text += f'{name}: {n}\n'

    await call.message.edit_text(text, reply_markup=ikb.admin_menu)
