from aiogram.types import *
from aiogram.dispatcher.filters import Text
from data.config import *
from loader import dp, bot
from utils.database import *
from keyboards import inline_keyboards as ikb
from states.state import *


#удаление валют


@dp.callback_query_handler(Text(startswith='delet_'))
async def delet_v(call: CallbackQuery):

    msg = call.data.replace('delet_', '')
  
    with DB() as db:
        req = db.give_keyboard_valute(type_valute=msg)

    await call.message.edit_text(f'Нажмите на валюту для ее удаления', reply_markup=ikb.delet_valute_key(valute_list=req))


@dp.callback_query_handler(Text(startswith='vdelet_'))
async def delete_valute_to_db(call: CallbackQuery):

    msg = call.data.split('_')
    
    with DB() as db:
        req = db.delete_valute(name=msg[1])

    if req:

        with DB() as db:
            req = db.give_keyboard_valute(type_valute=msg[2])

        await call.message.edit_text('Валюта удалена, если хотите удалить еще так же нажмиет на соответствующую кнопку', reply_markup=ikb.delet_valute_key(valute_list=req))

    else:

        await call.message.edit_text('Кажется, что то пошло не так, возникла ошика в баз данных...')