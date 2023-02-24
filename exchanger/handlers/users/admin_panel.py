from aiogram import types
from aiogram.types import *
from data.config import *
from loader import dp, bot
from utils.database import *
from utils.statistic_func import *
from keyboards import inline_keyboards as ikb
from aiogram.dispatcher import FSMContext
from states.state import *


#здесь находится основной функционал админ панели



@dp.message_handler(user_id = ADMIN_ID, commands=['admin'])
async def admin_panel(msg: types.Message):
	
	await msg.answer('Добро пожаловать в панель администратора!', reply_markup=ikb.admin_panel_key)


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='aspam')
async def aspam_func(call: types.CallbackQuery):

	await call.message.edit_text('Выберите вид рассылки\nС медиафайлами значит можно прикреплять гифки и фотографии', reply_markup=ikb.spam_key)


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='time_')
async def time_func(call: types.CallbackQuery):

	msg = call.data.replace('time_', '')

	with DB() as db:
		db_list = db.give_custom_history_db()

	ret = custom_stat_func(db_list, time=msg)

	await call.message.edit_text(ret, reply_markup=ikb.stat_back)


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='statistic')
async def statistic_func(call: types.CallbackQuery):

	with DB() as db:
		db_list = db.give_custom_history_db()

	with DB() as db:
		users = db.stat_user()

	activee = []
	noactive = []

	for i in users:
		if i[1] == '1':
			activee.append('1')
		else:
			noactive.append('0')

	a = all_stat(db_list)

	text = f'''
Всего юзеров: {len(users)}
Активных: {len(activee)}
Неактив: {len(noactive)}
{a}'''
	
	await call.message.edit_text(text, reply_markup=ikb.stat_time)



@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='status')
async def bot_func(call: types.CallbackQuery):

	with DB() as db:
		r = db.give_status_bot()

	await call.message.edit_text('В этом разделе вы можете выключить или включить бота по кнопке ниже', reply_markup=ikb.status_bot(status=r[0][1]))


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='sbot_')
async def sbot_func(call: types.CallbackQuery):

	msg = call.data.replace('sbot_', '')

	with DB() as db:
		r = db.on_off_bot(status=msg)

	with DB() as db:
		rr = db.give_status_bot()

	if r:
		await call.message.edit_text('✅ Статус бота изменен', reply_markup=ikb.status_bot(status=rr[0][1])) 

	else:
		await call.message.edit_text('❗️ Что то пошло не так, статус бота остался прежним', reply_markup=ikb.status_bot(status=rr[0][1])) 


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='adbanner')
async def banner_func(call: types.CallbackQuery):

	if call.data == 'adbanner_true':
		await Banner.text.set()

		await call.message.edit_text('Введите текст до 190 символов', reply_markup=ikb.admin_menu)

	else:		
		with DB() as db:
			r = db.move_banner(move='delete', text='false')

		if r:
			await call.answer('✅ Баннер удален из базы.')
		
		else:
			await call.message.edit_text('❕ Что то пошло не так...\nЕсли вы пытались удалить баннер проверьте, существует он или нет\nЕсли вы пытались добавить баннер то, скорее всего, он уже добавлен. Удалите старый баннер что бы добавить новый', reply_markup=ikb.admin_panel_key)


@dp.message_handler(state = Banner.text)
async def delete_channel(msg: types.Message, state = FSMContext):

	text = msg.text

	await state.finish()

	if len(text) > 190:
		await msg.answer(f'В вашем тексте: {len(text)} символов, допустимое значение 190 символов, попробуйте снова.', reply_markup=ikb.admin_panel_key)

	else:
		with DB() as db:
			r = db.move_banner(move='add', text=text)

		if r:
			await msg.answer('✅ Баннер добавлен в базу', reply_markup=ikb.admin_panel_key)
		
		else:
			await msg.answer('❕ Что то пошло не так...\nЕсли вы пытались удалить баннер проверьте, существует он или нет\nЕсли вы пытались добавить баннер то, скорее всего, он уже добавлен. Удалите старый баннер что бы добавить новый', reply_markup=ikb.admin_panel_key)


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='antiban')
async def antiban_func(call: types.CallbackQuery):

	await AntiBan.antiban_id.set()

	await call.message.edit_text('Введите id юзера, которого хотите разбанить', reply_markup=ikb.admin_menu)


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='channel')
async def channel_func(call: types.CallbackQuery, state: FSMContext):	

	if call.data == 'channel_add':
		await Channel.channel_info.set()

		await call.message.edit_text('➕ Что бы добавить канал для обязательной подписки юзера бота введите id канала и его ссылку через пробел\nНапример:\n-1001814613390 https://t.me/roegjreiog', reply_markup=ikb.admin_menu)

	else:
		await Channel.delet_channel.set()

		await call.message.edit_text('➕ Что бы удалить канал для обязательной подписки юзера бота введите id канала\nНапример:\n-1001814613390', reply_markup=ikb.admin_menu)


@dp.message_handler(state = Channel.delet_channel)
async def delete_channel(msg: types.Message, state = FSMContext):

	text = msg.text

	await state.finish()

	with DB() as db:
		r = db.delete_channel(id=text)

	if r:
		await msg.answer('👍 Канал успешно удален из базы данных.')
	
	else:
		await msg.answer('❕ Канал не был удален из базы данных, что то пошло не так, возможно, такого канала нету в базе.')


@dp.message_handler(state = Channel.channel_info)
async def set_channel(msg: types.Message, state = FSMContext):

	text = msg.text

	await state.finish()

	text = text.split(' ')

	with DB() as db:
		r = db.add_channel(id_channel=text[0], url=text[1])

	if r:
		await msg.answer('👍 Канал успешно добавле в базу данных.')
	
	else:
		await msg.answer('❕ Канал не был добвален в базу данных, что то пошло не так...')


@dp.callback_query_handler(user_id = ADMIN_ID, text_startswith='ban_user')
async def statsric_func(call: types.CallbackQuery, state: FSMContext):

	await Ban.ban_id.set()

	await call.message.edit_text('➕ Введите id юзера, которому хотите выдать бан', reply_markup=ikb.admin_menu)


@dp.message_handler(user_id = ADMIN_ID, state=Ban.ban_id)
async def ban_user(msg: types.Message, state: FSMContext):

	message = msg.text

	await state.finish()

	with DB() as db:
		req = db.ban_user(id=message)

	if req:
		await msg.answer(f'Пользователь успешно забанен!', reply_markup=ikb.admin_panel_key)

	else:
		await msg.answer(f'Что то пошло не так...', reply_markup=ikb.admin_panel_key)


@dp.message_handler(user_id = ADMIN_ID, state=AntiBan.antiban_id)
async def anti_ban_user(msg: types.Message, state: FSMContext):

	message = msg.text

	await state.finish()

	with DB() as db:
		req = db.anti_ban_user_to_db(id=message)

	if req:
		await msg.answer(f'Пользователь успешно разбанен!', reply_markup=ikb.admin_panel_key)

	else:
		await msg.answer(f'Что то пошло не так...', reply_markup=ikb.admin_panel_key)
