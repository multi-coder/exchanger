from aiogram import types
from aiogram.types import *
from aiogram.dispatcher.filters import Text
from data.config import *
from loader import dp, bot
from utils.database import *
from aiogram.dispatcher import FSMContext
from keyboards import inline_keyboards as ikb
from states.state import *


#здесь находится функционал добавленя валют


@dp.callback_query_handler(Text(startswith='add_'))
async def add_valute(call: types.CallbackQuery, state: FSMContext):

    type_ = call.data
    type_ = type_.split('_')

    async with state.proxy() as data:
        data['type_valute'] = type_[1]
        fiat = data['type_valute']

    await AddValute.log.set()

    if call.data == 'add_crypto':        
        await call.message.edit_text('🔤 Введите навзание криптовалюты, минимальную, максимальную сумму обмена и реквизит принятия средств, напрмиер:\n'
                        'Например:\n'
                        'BTC 0.0003 0.1433 bc1ief9g3jfjssghguaae93j2', reply_markup=ikb.admin_menu)

    elif call.data == 'add_fiat':
        await call.message.edit_text('🔤 Введите навзание фиата, минимальную, максимальную сумму обмена и реквизиты для оплаты\n'
                        'Например:\n'
                        'RUB 1000 15000 5536914000336929', reply_markup=ikb.admin_menu)


@dp.callback_query_handler(Text(startswith='back_to_admin'))
async def back_to_admin_func(call: types.CallbackQuery):

    await call.message.edit_text('💻 Главное меню панели администратора:', reply_markup=ikb.admin_panel_key)


@dp.message_handler(state=AddValute.log)
async def add_valute_to_db(msg: types.Message, state: FSMContext):

    message = msg.text
    message = message.split(' ')

    async with state.proxy() as data:
        type_valute = data['type_valute']

    await state.finish()

    if len(message) == 4:        
        with DB() as db:
            req = db.add_valute(valute=message[0], type=type_valute, min=message[1], max=message[2], requisite=message[3])

        if req:
            await msg.answer('✅ Валюта успешно добавлена в базу', reply_markup=ikb.admin_panel_key)

        else:
            await msg.answer('❗️ Не удалось добавить валюту в базу данных', reply_markup=ikb.admin_panel_key)

    else:
        await msg.answer('❗️ Формат лога введеный Вами неправилен!', reply_markup=ikb.admin_panel_key)