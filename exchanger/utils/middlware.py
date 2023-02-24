from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.types import *
from utils.database import *
from loader import dp, bot
from keyboards import inline_keyboards as ikb
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import asyncio
from loader import *
from aiogram.dispatcher.handler import CancelHandler, current_handler

#Разработчики: https://t.me/weaseldev @weaseldev


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.
    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator

#Разработчики: https://t.me/weaseldev @weaseldev

class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=2, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):

        handler = current_handler.get()

        dispatcher = Dispatcher.get_current()
        
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
          
            await self.message_throttled(call, t)

            raise CancelHandler()
#Разработчики: https://t.me/weaseldev @weaseldev
    async def message_throttled(self, call: types.CallbackQuery, throttled: Throttled):

        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 2:
            await call.answer('Дохуя шелестишь че то', show_alert=True)

        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)

        if thr.exceeded_count == throttled.exceeded_count:
            await call.answer('Проходи')




class OffMessage(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):

        for i in ADMIN_ID:
            if i == msg.from_id:
                pass
            else:
                with DB() as db:
                    r = db.give_status_bot()

                if r[0][1] == 'on':
                    pass
                else:
                    await msg.answer('🛑 Бот отключен ')
                    raise CancelHandler
                break


class OffCallback(BaseMiddleware):
    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        #Разработчики: https://t.me/weaseldev @weaseldev
        for i in ADMIN_ID:
            if i == call.from_user.id:
                pass
            else:
                with DB() as db:
                    r = db.give_status_bot()

                if r[0][1] == 'on':
                    pass
                else:
                    await call.answer('🛑 Бот отключен ', show_alert=True)
                    raise CancelHandler

                break
#Разработчики: https://t.me/weaseldev @weaseldev


class Ads(BaseMiddleware):
    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):

        with DB() as db:
            r = db.search_ban_user(id=call.from_user.id)
        
        if str(r[0]) == 'True':
            await call.answer('Вы забанены!', show_alert=True)
            raise CancelHandler

        else:
            if call.data == 'exchange':

                with DB() as db:
                    r = db.give_banner()

                if str(r) == '[]':
                    pass

                else:

                    text = r[0][1]
                    
                    await call.answer(text, show_alert=True)
#Разработчики: https://t.me/weaseldev @weaseldev

class SearchBanUserCallback(BaseMiddleware):
    async def pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        try:
            with DB() as db:
                r = db.search_ban_user(id=call.from_user.id)
            
            if str(r[0]) == 'True':
                await call.answer('Вы забанены!', show_alert=True)
                raise CancelHandler

            else:
                pass
        except:
            pass

class SearchBanUserMessage(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):
        
        try:
            with DB() as db:
                r = db.search_ban_user(id=msg.from_user.id)
            
            if str(r[0]) == 'True':
                await msg.answer('Вы забанены!')
                raise CancelHandler

            else:
                pass
        except CancelHandler as e:
            pass
            
      #Разработчики: https://t.me/weaseldev @weaseldev  
class SubsribeOnChannelMessage(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):

        with DB() as db:
            channel_list = db.give_list_channel()

    

        if str(channel_list) != '[]':
            
            url_list = []

            for i in channel_list:
                url_list.append(i[1])

#Разработчики: https://t.me/weaseldev @weaseldev

            for channel in channel_list:
                channel_id = channel[0]
                chat_link = channel[1].replace('https://t.me/', '@')
             
                user_channel_status = await bot.get_chat_member(chat_id=channel_id, user_id=msg.from_id)
                if user_channel_status["status"] != 'left':
                    pass
                else:
                    await bot.send_message(msg.from_user.id, '⁉️ Вы не подписались на один из каналов ниже, подпишитесь и нажмите на /start что бы продолжить пользоваться ботом!', reply_markup=ikb.channel_list(url_list))
                    raise CancelHandler
                    break

        else:
            pass


class SubsribeOnChannelCallback(BaseMiddleware):
    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):

        with DB() as db:
            channel_list = db.give_list_channel()

  #Разработчики: https://t.me/weaseldev @weaseldev
        if str(channel_list) != '[]':
            
            url_list = []

            for i in channel_list:
                url_list.append(i[1])



            for channel in channel_list:
                channel_id = channel[0]
                chat_link = channel[1].replace('https://t.me/', '@')
                
                user_channel_status = await bot.get_chat_member(chat_id=channel_id, user_id=call.from_user.id)
                if user_channel_status["status"] != 'left':
                    pass
                else:
                    await bot.send_message(call.from_user.id, '⁉️ Вы не подписались на один из каналов ниже, подпишитесь и нажмите на /start что бы продолжить пользоваться ботом!', reply_markup=ikb.channel_list(url_list))
                    
                    raise CancelHandler
                    break
#Разработчики: https://t.me/weaseldev @weaseldev
        else:
            pass