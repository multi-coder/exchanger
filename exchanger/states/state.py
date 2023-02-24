from aiogram.dispatcher.filters.state import State, StatesGroup

#Разработчики: https://t.me/weaseldev @weaseldev
class AddValute(StatesGroup):

    type_valute = State()
    log = State()

class Ban(StatesGroup):

    ban_id = State()


class AntiBan(StatesGroup):

    antiban_id = State()


class Payment(StatesGroup):

    type_valute = State()
    payment_metod = State()
#Разработчики: https://t.me/weaseldev @weaseldev

class Exchange(StatesGroup):

    valute_exhcnage = State()
    valute_issue = State()
    payment_method = State()
    amount = State()
    requisites = State()
    comment = State()
    send_to_false = State()


class Exchange1(StatesGroup):

    valute_exhcnage = State()
    valute_issue = State()
    payment_method = State()
    amount = State()
    requisites = State()
    comment = State()
    send_to_false = State()


class Channel(StatesGroup):

    channel_info = State()
    delet_channel = State()

class Banner(StatesGroup):
#Разработчики: https://t.me/weaseldev @weaseldev
    text = State()

class Spam(StatesGroup):

    text = State()
    send = State()

class SpamMedia(StatesGroup):

    text = State()
    file_id = State()
    send = State()