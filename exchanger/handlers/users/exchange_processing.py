from aiogram import types
from aiogram.types import *
from data.config import *
from loader import dp, bot
from keyboards import inline_keyboards as ikb
from utils.database import *
from states.state import *
from aiogram.dispatcher.filters import Text
from datetime import date


#процесс обмена


@dp.callback_query_handler(Text(startswith='anket_'))
async def set_anket(call: types.CallbackQuery):

    msg = call.data
    msg_text = call.message.text.split('\n')

    if 'anket_false' in msg:
        await call.message.edit_text(f'Вы отклонили заявку от пользователя:\n'
                                f'{msg_text[2]}\n{msg_text[3]}\n{msg_text[4]}\n\n'
                                f'{msg_text[9]}\n'
                                f'{msg_text[8]}', reply_markup=ikb.close_key)

        msg = msg.split('_')

        text = f'''
😔 Ваша заявка обмена {msg[5]} {msg[3]} на {msg[4]} была отклонена.'''

        await bot.send_message(int(msg[2]), text, reply_markup=ikb.close_key)

    else:
        await call.message.edit_text(f'Вы одобрили заявку от пользователя:\n'
                                f'{msg_text[2]}\n{msg_text[3]}\n{msg_text[4]}\n\n'
                                f'{msg_text[9]}\n'
                                f'{msg_text[8]}', reply_markup=ikb.close_key)

        msg = msg.split('_')

        with DB() as db:
            req = db.give_info_valute(name=f'{msg[2]}')

        exchange = f'{msg[2]}_{msg[3]}'

        await bot.send_message(int(msg[1]), f'🔄 Ваша заявка обмена <code>{msg[2]}</code> на <code>{msg[3]}</code> была одобрена, переведите <code>{msg[4]}</code> {msg[2]} на следущий адрес:\n'
                                        f'<code>{str(req[0][0])}</code>\n'
                                        f'После перевода средств нажмите на кнопку ниже', reply_markup=ikb.anket_step_two(exchange, amount=msg[4]))


@dp.callback_query_handler(Text(startswith='usanket_'))
async def true_anket(call: types.CallbackQuery):

    msg = call.data.split('_')

    if msg[1] == 'false':
        await call.message.edit_text('Вы отменили сделку', reply_markup=ikb.close_key)

        for i in ADMIN_ID:
            await bot.send_message(int(i), '❕ Уведомоение\n\n'
                                            '😕 Пользователь отменил сделку:\n'
                                            f'🆔: <code>{call.from_user.id}</code>\n'
                                            f'👾 Username: @{call.from_user.username}\n'
                                            f'👤 Имя: <code>{call.from_user.full_name}</code>\n\n', reply_markup=ikb.close_key)

    else:
        await call.message.edit_text('Ожидайте поступление средств, в случае чего можно связаться с саппортом по кнопке ниже', reply_markup=ikb.supprot_key)

        for id_ in ANKET_SEND:

            text = f'''
Пользователь подтверил перевод средств:
🆔: <code>{call.from_user.id}</code>
👾 Username: @{call.from_user.username}
👤 Имя: <code>{call.from_user.full_name}</code>
Обмен {msg[4]} {msg[2]} на {msg[3]}
'''

            await bot.send_message(int(id_), text, reply_markup=ikb.confirm_exchange(id=call.from_user.id, exchange=f'{msg[2]}_{msg[3]}', amount=f'{msg[4]}'))


@dp.callback_query_handler(Text(startswith='confirm_'))
async def confirm_anket(call: types.CallbackQuery):

    msg = call.data.split('_')

    if msg[1] == 'false':
        await call.message.edit_text('⁉️ Вы отменили обмен, пользователю было отправлено сообщение о том, что нужно обратиться к саппорту что бы вернуть сердства.', reply_markup=ikb.close_key)

        await bot.send_message(int(msg[2]), f'❓ По каким то причинам Ваш обмен {msg[3]} {msg[4]} на {msg[5]} был отменен, напишите саппорту проекта для возврата средств', reply_markup=ikb.supprot_key)

    else:
        await call.message.edit_text('✅ Сделка завершена, пользователь был уведомлен.', reply_markup=ikb.close_key)

        await bot.send_message(int(msg[2]), '🎉 Администратор отправил средства на ваши реквизиты', reply_markup=ikb.close_key)

        dt_now = date.today()

        with DB() as db:
            a = db.add_history(amount=msg[3], id=msg[2], name_exchange=msg[4])

        if a:
            await call.message.edit_text('✅ Сделка завершена, пользователь был уведомлен, сделка занесена в базу данных.', reply_markup=ikb.close_key)
        
        else:
            await call.message.edit_text('✅ Сделка завершена, пользователь был уведомлен, но по каким то причинам сделка не была занесена в базу данных.', reply_markup=ikb.close_key)



