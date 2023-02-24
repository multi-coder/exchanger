from aiogram import types
from aiogram.types import *
from aiogram.dispatcher.filters import Text
from data.config import *
from loader import dp, bot
from utils.database import *
from aiogram.dispatcher import FSMContext
from keyboards import inline_keyboards as ikb
from states.state import *


#здесь находится функционал удаления и добавления методов выплаты


@dp.callback_query_handler(Text(startswith='dpayment_'), user_id = ADMIN_ID)
async def del_payment_method(call: types.CallbackQuery):

    msg = call.data.replace('dpayment_', '')

    with DB() as db:
        req = db.give_payment_method(type=msg)

    await call.message.edit_text(f'Нажмите на метод выплаты, который хотите удалить:', reply_markup=ikb.delet_payment_key(req))


@dp.callback_query_handler(Text(startswith='methoddel_'), user_id = ADMIN_ID)
async def delpay(call: types.CallbackQuery):

    msg = call.data.split('_')

    with DB() as db:
        r = db.add_or_delet_payment_method(name=msg[2], type=msg[1], move='delete')

    with DB() as db:
        req = db.give_payment_method(type=msg[1])

    if r:
        await call.message.edit_text(f'Нажмите на метод выплаты, который хотите удалить:', reply_markup=ikb.delet_payment_key(req))

    else:
        await call.message.edit_text(f'Произошла ошибка, не удалось удалить метод выплаты', reply_markup=ikb.delet_payment_key(req))


@dp.callback_query_handler(Text(startswith='payment_'), user_id = ADMIN_ID)
async def add_payment_method(call: types.CallbackQuery, state: FSMContext):

    msg = call.data.replace('payment_', '')

    async with state.proxy() as data:
        data['type_valute'] = msg

    await Payment.payment_metod.set()

    if msg == 'crypto':
        await call.message.edit_text('Введите платежные системы для выплаты обмена криптовалюты через ":"\n'
                                    'Например:\n'
                                    'Тинькофф:ВТБ:QIWI Кошелек:Альфа Банк', reply_markup=ikb.admin_menu)
    
    else:
        await call.message.edit_text('Введите платежные системы для выплаты обмена фиата через ":"\n'
                                    'Например:\n'
                                    'Binance:BTC:ETH', reply_markup=ikb.admin_menu)


@dp.message_handler(state = Payment.payment_metod)
async def add_method_to_dp(msg: types.Message, state: FSMContext):

    message = msg.text.split(':')

    async with state.proxy() as data:
        type_ = data['type_valute']

    await state.finish()

    with DB() as db:
        for name in message:
            req = db.add_or_delet_payment_method(name=name, type=type_, move='add')

            if req:
                pass
            
            else:
                await msg.answer(f'Произошла ошибка при добавлении {name}')

    await msg.answer('Добавление методов вылпат заверешна.', reply_markup=ikb.admin_panel_key)

