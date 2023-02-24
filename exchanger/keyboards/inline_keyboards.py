from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import *
from aiogram.types.web_app_info import WebAppInfo

main_menu_inline = InlineKeyboardMarkup()
main_menu_inline.row(InlineKeyboardButton('👤 Профиль', callback_data='profile'),
                    InlineKeyboardButton('🔄 Обмен', callback_data='exchange'))
main_menu_inline.row(InlineKeyboardButton('ℹ️ ЧаВо?', callback_data='faq'),
                    InlineKeyboardButton('👁‍🗨 Саппорт', url=SUPPORT_LINK))
#Разработчики: https://t.me/weaseldev @weaseldev
def channel_list(channels):
    channel = InlineKeyboardMarkup()
    for i in channels:
        channel.row(InlineKeyboardButton('➕ Канал', url = i))
    return channel


stat_time = InlineKeyboardMarkup()
stat_time.row(InlineKeyboardButton('🕐 За день', callback_data='time_day'))
stat_time.row(InlineKeyboardButton('🕒 За неделю', callback_data='time_week'))
stat_time.row(InlineKeyboardButton('🕕 За месяц', callback_data='time_month'))
stat_time.row(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_admin'))


stat_back = InlineKeyboardMarkup()
stat_back.row(InlineKeyboardButton('⬅️ Назад', callback_data='statistic'))

#Разработчики: https://t.me/weaseldev @weaseldev

back_to_menu = InlineKeyboardMarkup()
back_to_menu.row(InlineKeyboardButton('⏪ Назад', callback_data=f'menu'))


exchange_valute = InlineKeyboardMarkup()
exchange_valute.row(InlineKeyboardButton('Фиат на крипту', callback_data='fiat_to_crypto'))
exchange_valute.row(InlineKeyboardButton('Крипту на фиат', callback_data='crypto_to_fiat'))
exchange_valute.row(InlineKeyboardButton('⏪ Назад', callback_data=f'menu'))


admin_panel_key = InlineKeyboardMarkup()
admin_panel_key.row(InlineKeyboardButton('➕ Добавить фиат', callback_data=f'add_fiat'),
                    InlineKeyboardButton('➕ Добавить крипту', callback_data=f'add_crypto'))
admin_panel_key.row(InlineKeyboardButton('➖ Удалить фиат', callback_data=f'delet_fiat'),
                    InlineKeyboardButton('➖ Удалить крипту', callback_data=f'delet_crypto'))
admin_panel_key.row(InlineKeyboardButton('➕ Выплаты фиата', callback_data=f'payment_fiat'),
                    InlineKeyboardButton('➕ Выплаты крипты', callback_data=f'payment_crypto'))
admin_panel_key.row(InlineKeyboardButton('➖ Удалить фиат выплату', callback_data=f'dpayment_fiat'),
                    InlineKeyboardButton('➖ Удалить крипто выплату', callback_data=f'dpayment_crypto'))                
admin_panel_key.row(InlineKeyboardButton('♻️ Разбанить', callback_data='antiban'),
                    InlineKeyboardButton('📛 Выдать бан', callback_data=f'ban_user'))
admin_panel_key.row(InlineKeyboardButton('📊 Статистика', callback_data='statistic'),
                    InlineKeyboardButton('📣 Расылка', callback_data='aspam'))
admin_panel_key.row(InlineKeyboardButton('➕ Привязать канал', callback_data='channel_add'),
                    InlineKeyboardButton('➖ Отвязать канал', callback_data='channel_delet'))
admin_panel_key.row(InlineKeyboardButton('➕ Добавить рекламу', callback_data=f'adbanner_true'),
                    InlineKeyboardButton('➖ Удалить рекламу', callback_data=f'adbanner_false'))
admin_panel_key.row(InlineKeyboardButton('🔄 Изменить статус бота', callback_data=f'status'))
                    
#Разработчики: https://t.me/weaseldev @weaseldev


def status_bot(status):
    status_key = InlineKeyboardMarkup()
    if status == 'on':
        status_key.row(InlineKeyboardButton('🔴 Выключить', callback_data=f'sbot_off'))
    else:
        status_key.row(InlineKeyboardButton('🟢 Включить', callback_data=f'sbot_on'))
    status_key.row(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_admin'))
    return status_key


close_key = InlineKeyboardMarkup()
close_key.row(InlineKeyboardButton('✖️ Закрыть ✖️', callback_data='close'))

supprot_key = InlineKeyboardMarkup()
supprot_key.row(InlineKeyboardButton('👁‍🗨 Саппорт', url=SUPPORT_LINK))
supprot_key.row(InlineKeyboardButton('✖️ Закрыть ✖️', callback_data='close'))


spam_key = InlineKeyboardMarkup()
spam_key.row(InlineKeyboardButton('📷 С медиафайлом', callback_data='spam_yesphoto'))
spam_key.row(InlineKeyboardButton('📝 Без медифайла', callback_data='spam_nophoto'))
spam_key.row(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_admin'))

#Разработчики: https://t.me/weaseldev @weaseldev

spam_key_two = InlineKeyboardMarkup()
spam_key_two.row(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_admin'))


go_spam = InlineKeyboardMarkup()
go_spam.row(InlineKeyboardButton('✅ Начать', callback_data='ps_go'))
go_spam.row(InlineKeyboardButton('❌ Отмена', callback_data='back_to_admin'))

admin_menu = InlineKeyboardMarkup()
admin_menu.row(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_admin'))


def delet_payment_key(payment_list):

    delet_payment = InlineKeyboardMarkup()

    for log in payment_list:

        name = log[0]
        type_ = log[1]

        delet_payment.row(InlineKeyboardButton(f'{name}', callback_data=f'methoddel_{type_}_{name}'))
    delet_payment.row(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_admin'))
    return delet_payment

#Разработчики: https://t.me/weaseldev @weaseldev


def delet_valute_key(valute_list):

    delet_valute = InlineKeyboardMarkup()

    for log in valute_list:
        
        name = log[0]
        type_ = log[1]

        delet_valute.row(InlineKeyboardButton(f'{name}', callback_data=f'vdelet_{name}_{type_}'))
    delet_valute.row(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_admin'))

    return delet_valute

#Разработчики: https://t.me/weaseldev @weaseldev

def exchange_user(valute_list, type_):

    exchange_user_key = InlineKeyboardMarkup()

    if type_ == 'crypto':

        for log in valute_list:

            if log[1] == 'crypto':

                exchange_user_key.row(InlineKeyboardButton(log[0], callback_data=f'exchange_{log[0]}'))
            else:
                pass

    else:

        for log in valute_list:

            if log[1] == 'fiat':

                exchange_user_key.row(InlineKeyboardButton(log[0], callback_data=f'exchange_{log[0]}'))
            else:
                pass
    exchange_user_key.row(InlineKeyboardButton('⏪ Назад', callback_data=f'menu'))
    return exchange_user_key

#Разработчики: https://t.me/weaseldev @weaseldev

def give_payment_method_key(type_):

    key_payment = InlineKeyboardMarkup()

    for log in type_:

        name = log[0]
        type_ = log[1]

        key_payment.row(InlineKeyboardButton(f'{name}', callback_data=f'pmethod_{name}'))
    key_payment.row(InlineKeyboardButton('⬅️ Назад', callback_data='menu'))
    return key_payment



send_admin_key = InlineKeyboardMarkup()
send_admin_key.row(InlineKeyboardButton('↗️ Отправить', callback_data=f'asend'),
                InlineKeyboardButton('↩️ Отмена', callback_data='menu'))


def anket_user(id, exchange, amount):

    user_anket_key = InlineKeyboardMarkup()
    user_anket_key.row(InlineKeyboardButton('✅ Принять', callback_data=f'anket_{id}_{exchange}_{amount}'),
                    InlineKeyboardButton('❌ Отклонить', callback_data=f'anket_false_{id}_{exchange}_{amount}'))
    return user_anket_key
    
#Разработчики: https://t.me/weaseldev @weaseldev

def anket_step_two(exchange, amount):

    anket_user_key = InlineKeyboardMarkup()
    anket_user_key.row(InlineKeyboardButton('✅ Перевел', callback_data=f'usanket_true_{exchange}_{amount}'),
                        InlineKeyboardButton('❌ Отменить обмен', callback_data=f'usanket_false_{exchange}_{amount}'))
    return anket_user_key
    

def confirm_exchange(id, exchange, amount):

    confirm_key = InlineKeyboardMarkup()
    confirm_key.row(InlineKeyboardButton('Закончить обмен', callback_data=f'confirm_good_{id}_{amount}_{exchange}'))
    confirm_key.row(InlineKeyboardButton('Отменить обмен', callback_data=f'confirm_false_{id}_{amount}_{exchange}'))
    return confirm_key