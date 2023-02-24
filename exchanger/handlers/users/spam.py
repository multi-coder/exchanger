from aiogram import types
from aiogram.types import *
from data.config import *
from loader import dp, bot
from utils.database import *
from keyboards import inline_keyboards as ikb
from aiogram.dispatcher import FSMContext
from states.state import *



#функция рассылки



@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='spam_')
async def time_func(call: types.CallbackQuery):

    msg = call.data.replace('spam_', '')

    if msg == 'nophoto':

        await Spam.text.set()

        await call.message.edit_text('Введите текст', reply_markup=ikb.spam_key_two)

    else:

        await SpamMedia.text.set()

        await call.message.edit_text('Введите ТОЛЬКО ТЕКСТ!!!', reply_markup=ikb.spam_key_two)


@dp.message_handler(user_id = ADMIN_ID, state = SpamMedia.text)
async def set_text_media(msg: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['text'] = msg.html_text

    await SpamMedia.file_id.set()

    await msg.answer('Отправьте фотографию или гифку ДО 20МБ !!!', reply_markup=ikb.admin_menu)


@dp.message_handler(user_id = ADMIN_ID, content_types=['photo'], state = SpamMedia.file_id)
async def set_text_media(msg: types.Message, state: FSMContext):

    id_photo = msg.photo[-1].file_id
    async with state.proxy() as data:
        data['file_id'] = id_photo
        text = data['text']  

    await SpamMedia.send.set()

    await msg.answer_photo(photo=id_photo, caption=f'Ваш пост выглядит так:\n{text}\nНачать рассылку?', reply_markup=ikb.go_spam)


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='ps_go', state=SpamMedia.send)
async def time_func(call: types.CallbackQuery, state: FSMContext):

    await call.message.edit_caption('🕠 Ожидайте окончания рассылки, Вам придет отчет', reply_markup=ikb.close_key)

    async with state.proxy() as data:
        text = data['text']
        file_id = data['file_id']

    await state.finish()

    with DB() as db:
        ids = db.give_id_user()

    good = 0
    false = 0
    for id_ in ids:


        try:
            await bot.send_photo(int(id_[0]), photo=file_id, caption=text) 
            good += 1
        except Exception as e:
        
            with DB() as db:
                a = db.unable_user(id_[0])
            false +=1

    ot = f'''
📊 Отчет о рассылке:

👥 Всего людей в базе: {len(ids)}
👤 Активных: {good}
👤 Неактивных: {false}'''

    await bot.send_message(call.from_user.id, ot, reply_markup=ikb.admin_panel_key)


@dp.message_handler(user_id = ADMIN_ID, state = Spam.text)
async def set_text(msg: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['text'] = msg.html_text

    await Spam.send.set()

    await msg.answer('Ваш текст выглядит так:\n'
                    f'{msg.html_text}', reply_markup=ikb.go_spam)


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='ps_go', state=Spam.send)
async def time_func(call: types.CallbackQuery, state: FSMContext):

    await call.message.edit_text('🕠 Ожидайте окончания рассылки, Вам придет отчет', reply_markup=ikb.close_key)

    async with state.proxy() as data:
        text = data['text']

    await state.finish()

    with DB() as db:
        ids = db.give_id_user()

    good = 0
    false = 0
    for id_ in ids:

        try:
            await bot.send_message(int(id_[0]), text) 
            good += 1
        except Exception as e:
        
            with DB() as db:
                db.unable_user(id_[0])
            false +=1

    ot = f'''
📊 Отчет о рассылке:

👥 Всего людей в базе: {len(ids)}
👤 Активных: {good}
👤 Неактивных: {false}'''

    await bot.send_message(call.from_user.id, ot, reply_markup=ikb.close_key)
            