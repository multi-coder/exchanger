from aiogram import types
from aiogram.types import *
from data.config import *
from loader import dp, bot
from keyboards import inline_keyboards as ikb
from utils.database import *
from states.state import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


#обмен фиата на крипту


@dp.callback_query_handler(text_startswith="fiat_to_crypto")
async def fiat_to_crypto_handler(call: types.CallbackQuery):
    
    with DB() as db:
        list_key = db.give_keyboard_valute(type_valute='fiat')

    await Exchange1.valute_exhcnage.set()

    await call.message.edit_text(f'Выберите валюту, которую Вы хотите обменять', reply_markup=ikb.exchange_user(valute_list=list_key, type_='fiat'))


@dp.callback_query_handler(Text(startswith='exchange_'), state = Exchange1.valute_exhcnage)
async def set_excahnge_fiat(call: types.CallbackQuery, state: FSMContext):

    msg = call.data.replace('exchange_', '')

    async with state.proxy() as data:
        data['valute_exhcnage'] = msg

    with DB() as db:
        list_key = db.give_keyboard_valute(type_valute='crypto')

    await Exchange1.valute_issue.set()

    await call.message.edit_text(f'Выберите криптовалюту, которую Вы хотите получить', reply_markup=ikb.exchange_user(valute_list=list_key, type_='crypto'))
    

@dp.callback_query_handler(Text(startswith='exchange_'), state = Exchange1.valute_issue)
async def set_issue(call: types.CallbackQuery, state: FSMContext):

    msg = call.data.replace('exchange_', '')

    async with state.proxy() as data:
        data['valute_issue'] = msg
        name = data['valute_exhcnage']

    await Exchange1.payment_method.set()

    with DB() as db:
        req = db.give_payment_method(type='fiat')

    await call.message.edit_text(f'Выберите метод выплаты:', reply_markup=ikb.give_payment_method_key(type_=req))


@dp.callback_query_handler(Text(startswith='pmethod_'), state = Exchange1.payment_method)
async def set_issue(call: types.CallbackQuery, state: FSMContext):

    msg = call.data.replace('pmethod_', '')

    async with state.proxy() as data:
        data['payment_method'] = msg
        name = data['valute_exhcnage']

    await Exchange1.amount.set()

    with DB() as db:
        req = db.give_min_and_max(name=name)

    await call.message.edit_text(f'Минимальная сумма для обмена {name}: {req[0][0]}\n'
                                f'Максимальная сумма для обмена {name}: {req[0][1]}\n'
                                f'Введите колличество {name}, которое Вы хотите обменять:', reply_markup=ikb.back_to_menu)


@dp.message_handler(state = Exchange1.amount)
async def set_issue(message: types.Message, state: FSMContext):

    msg = message.text

    try:
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id-1)

    except:
        pass

    async with state.proxy() as data:
        name = data['valute_exhcnage']

    with DB() as db:
        req = db.give_min_and_max(name=name)

    try:
        amount = float(msg)

        if amount < float(req[0][0]) or amount > float(req[0][1]):
            await message.answer(text=f'Вы ввели сумму, которая не соответствует минимуму и максимуму для данной валюты\n'
                                f'Минимальная сумма для обмена {name}: {req[0][0]}\n'
                                f'Максимальная сумма для обмена {name}: {req[0][1]}\n'
                                f'Введите колличество {name}, которое Вы хотите обменять:', reply_markup=ikb.back_to_menu)

        else:
            async with state.proxy() as data:
                data['amount'] = amount

            await Exchange1.requisites.set()

            await message.answer('Введите реквизиты выплаты, например криптокошелек для принятия средств', reply_markup=ikb.back_to_menu)

    except Exception as e:
        await message.answer(f'Вы указали не число!\n'
                            f'Минимальная сумма для обмена {name}: {req[0][0]}\n'
                            f'Максимальная сумма для обмена {name}: {req[0][1]}\n'
                            f'Введите колличество {name}, которое Вы хотите обменять:', reply_markup=ikb.back_to_menu)


@dp.message_handler(state = Exchange1.requisites)
async def set_requisites(message: types.Message, state: FSMContext):

    msg = message.text

    try:
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id-1)

    except:
        pass

    async with state.proxy() as data:
        data['requisites'] = msg

    await Exchange1.comment.set()

    await message.answer('Введите комментарий, если он тут не нужен отправьте любой символ:', reply_markup=ikb.back_to_menu)


@dp.message_handler(state = Exchange1.comment)
async def set_comment(message: types.Message, state: FSMContext):

    msg = message.text

    id = message.from_id

    try:
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id=message.message_id-1)

    except:
        pass

    async with state.proxy() as data:
        data['comment'] = msg
        valute_exhcnage = data['valute_exhcnage']
        valute_issue = data['valute_issue']
        payment_method = data['payment_method']
        amount = data['amount']
        requisites = data['requisites']
        
    application = f'''
Ваша заявка выглядит так:

🔄 Нужно обменять {valute_exhcnage} на {valute_issue}
💸 Выплатить на {payment_method}
💰 Колличестов {valute_exhcnage}: {amount}
💳 Реквизиты: {requisites}
✉️ Комментарий: {msg}

🗳 Отправить заявку на рассмотрение?
'''

    await Exchange1.send_to_false.set()

    await message.answer(application, reply_markup=ikb.send_admin_key)
        
    
@dp.callback_query_handler(Text(startswith='asend'), state = Exchange1.send_to_false)
async def set_send_to_false(call: types.CallbackQuery, state: FSMContext):

    id = call.from_user.id

    async with state.proxy() as data:
        valute_exhcnage = data['valute_exhcnage']
        valute_issue = data['valute_issue']
        payment_method = data['payment_method']
        amount = data['amount']
        requisites = data['requisites']
        comment = data['comment']

    await state.finish()

    await call.message.edit_text('✅ Вашая заявка отправлена на рассмотрение, ожидайте отклика администрации.', reply_markup=ikb.main_menu_inline)

    for id_ in ANKET_SEND:
        text = f'''
Поступила новая заявка:

🆔: <code>{id}</code>
👾 Username: @{call.from_user.username}
👤 Имя: <code>{call.from_user.full_name}</code>

🔄 Нужно обменять {valute_exhcnage} на {valute_issue}
💸 Выплатить на {payment_method}
💰 Колличестов {valute_exhcnage}: {amount}
💳 Реквизиты: {requisites}
✉️ Комментарий: {comment}'''

        await bot.send_message(id_, text, reply_markup=ikb.anket_user(id=id, exchange=f'{valute_exhcnage}_{valute_issue}', amount=amount))