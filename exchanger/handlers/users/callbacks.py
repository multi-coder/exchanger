from aiogram import types
from aiogram.types import *
from data.config import *
from loader import dp, bot
from keyboards import inline_keyboards as ikb
from aiogram.dispatcher.filters import Text
from states.state import *
from aiogram.dispatcher import FSMContext
from utils.middlware import *


#обработка коллбеков


@dp.callback_query_handler(text_startswith='close')
async def close_message(call: types.CallbackQuery):

    await call.message.delete()


@dp.callback_query_handler(text_startswith="profile")
async def profile_handler(call: types.CallbackQuery):

    await bot.answer_callback_query(call.id)

    await call.message.edit_text(f'ID: <code>{call.from_user.id}</code>\n', 
                               reply_markup=ikb.back_to_menu)


@dp.callback_query_handler(text_startswith="menu")
async def profile_handler(call: types.CallbackQuery):

    await call.message.edit_text('Добро пожаловать в обменник!', reply_markup=ikb.main_menu_inline)


@dp.callback_query_handler(text_startswith="faq")
async def faq_handler(call: types.CallbackQuery):

    await call.message.edit_text(FAQ, reply_markup=ikb.back_to_menu)


@dp.callback_query_handler(text_startswith="exchange")
async def exchange_handler(call: types.CallbackQuery):

    await call.message.edit_text('Какой обмен нужно совершить?', reply_markup=ikb.exchange_valute)


@dp.callback_query_handler(Text(startswith='back_to_admin'), state="*")
async def back_to_admin_func(call: types.CallbackQuery, state: FSMContext):

    try:
        await state.finish()
        await call.message.edit_text('💻 Главное меню панели администратора:', reply_markup=ikb.admin_panel_key)

    except Exception as e:
        await call.message.delete()
        await bot.send_message(call.from_user.id, '💻 Главное меню панели администратора:', reply_markup=ikb.admin_panel_key)


@dp.callback_query_handler(Text(startswith='menu'), state="*")
async def back_to_menu_user(call: types.CallbackQuery, state: FSMContext):

    await state.finish()

    await call.message.edit_text('Вы были перенаправлены в главное меню', reply_markup=ikb.main_menu_inline)
    