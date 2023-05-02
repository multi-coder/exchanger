import sqlite3, requests, bs4
from data.config import *
from datetime import date
import datetime


class DB(object):
    def __init__(self, db_fp=f'data/data.db'):
        self.db_fp = db_fp
        self.headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
        self.base = sqlite3.connect(self.db_fp, check_same_thread=False)
        self.cur = self.base.cursor()
        self.create_tables()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.base.commit()
        self.cur.close()
        self.base.close()


    def create_tables(self):
        self.base.execute("""CREATE TABLE IF NOT EXISTS users(
                    id PRIMARY KEY, 
                    name_user TEXT,
                    username TEXT,
                    ban TEXT,
                    active TEXT)""")
        self.base.execute('CREATE TABLE IF NOT EXISTS payment_method(name TEXT PRIMARY KEY, type TEXT)')
        self.base.execute('CREATE TABLE IF NOT EXISTS valute(name TEXT PRIMARY KEY, type TEXT, minimal TEXT, maximal TEXT, requisite TEXT)')
        self.base.execute('CREATE TABLE IF NOT EXISTS chanel(id_channel TEXT PRIMARY KEY, url TEXT)')
        self.base.execute('CREATE TABLE IF NOT EXISTS banner(id TEXT PRIMARY KEY, text TEXT)')        
        self.base.execute('CREATE TABLE IF NOT EXISTS status_active(id TEXT PRIMARY KEY, status TEXT)')
        try:
            self.cur.execute('INSERT INTO status_active VALUES(?, ?)', ['1', 'on'])
        except:
            pass
        self.base.execute('CREATE TABLE IF NOT EXISTS {}(amount TEXT, id TEXT, exchange TEXT, data TEXT)'.format('history'))
        self.base.commit()

    def add_history(self, amount, id, name_exchange):

        week_number = datetime.datetime.today().isocalendar()[1]

        dt_now = date.today()

        dt_now = f'{dt_now}-{str(week_number)}'

        try:
            self.cur.execute('INSERT INTO history VALUES(?, ?, ?, ?)',
                    [str(amount), str(id), str(name_exchange), str(dt_now)])
            self.base.commit()
        except Exception as e:
            print(f'ОШибка в добавлении в историю :{e}')

    def give_custom_history_db(self):
        
        try:
            r = self.cur.execute('SELECT * FROM history').fetchall()
            return r

        except Exception as e:
            print(f'ОШибка при выдаче кастомной итории: {e}')
            return False








    def give_status_bot(self):

        r = self.cur.execute('SELECT * FROM status_active').fetchall()
        return r

    def on_off_bot(self, status):

        self.cur.execute(f'UPDATE status_active SET status = ? WHERE id = ?', [status, '1'])
        self.base.commit()
        return True

    def give_banner(self):

        req = self.cur.execute('SELECT * FROM banner').fetchall()
        return req


    def move_banner(self, move, text):

        try:
            if move == 'add':

                try:
                    self.cur.execute('INSERT INTO banner VALUES(?, ?)', ['1', text])
                    self.base.commit()
                    return True

                except Exception as e:
                    return False

            else:

                try:
                    self.cur.execute('DELETE FROM banner WHERE id = ?', ['1'])
                    self.base.commit()
                    return True

                except Exception as e:
                    return False


        except Exception as e:
            print(f'Ошибка при работе с баннером: {e}')
            return False


    def delete_channel(self, id):

        try:
            self.cur.execute('DELETE FROM chanel WHERE id = ?', [str(id)])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка при удалении канала: {e}')
            return False


    def add_channel(self, id_channel, url):

        try:
            self.cur.execute('INSERT INTO chanel VALUES(?, ?)', [str(id_channel), str(url)])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка при добавления канала: {e}')
            return False

    def give_list_channel(self):

        req = self.cur.execute('SELECT * FROM chanel').fetchall()
        return req


    def give_stat_admin(self):

        try:
            req = self.cur.execute('SELECT * FROM stat').fetchall()
            return req
        
        except Exception as e:
            print(f'ОШибка при выдаче статистики: {e}')

    def add_seccesful_exchange(self, id, exchange, amount, data):

        try:
            self.cur.execute('INSERT INTO stat VALUES(?, ?, ?, ?)', [str(id), str(exchange), str(amount), str(data)])
            self.base.commit()
            return True

        except Exception as e:
            print(f'ОШибка при занесении сделки в базу: {e}')
            return False

    def add_or_delet_payment_method(self, name, type, move):

        if move == 'add':

            try:
                self.cur.execute('INSERT INTO payment_method VALUES(?, ?)', [str(name), str(type)])
                self.base.commit()
                return True

            except Exception as e:
                print(f'Ошибка при добавлении или дуалении из базы метода выплаты: {e}')
                return False

        elif move == 'delete':

            try:
                self.cur.execute('DELETE FROM payment_method WHERE name = ?', [name])
                self.base.commit()
                return True

            except Exception as e:
                print(f'Ошибка при удалении метода выплаты: {e}')
                return False

        else:
            return False


    def give_payment_method(self, type):

        try:
            req = self.cur.execute('SELECT * FROM payment_method WHERE type = ?', [type]).fetchall()
            return req

        except Exception as e:
            print(f'Ошибка при выдаче мотодов выплат: {e}')
            return False

    def unable_user(self, id):

        try:
            self.cur.execute(f'UPDATE users SET active = ? WHERE id = ?', ['0', str(id)])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка при выдаче неактива пользователю: {e}')
            return False

    def stat_user(self):
        try:
            req = self.cur.execute('SELECT id, active FROM users').fetchall()
            return req
        except Exception as e:
            print(e)

    def give_id_user(self):
        try:
            req = self.cur.execute('SELECT id FROM users').fetchall()
            return req
        except Exception as e:
            print(e)


    def add_user(self, id, name_user, username):
        
        try:
            self.cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?)', [str(id), name_user, username, 'None', '1'])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка при добавлении пользователя в базу: {e}')
            return False


    def ban_user(self, id):

        try:
            self.cur.execute(f'UPDATE users SET ban = ? WHERE id = ?', ['True', str(id)])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка рип бане пользователя: {e}')
            return False

    
    def anti_ban_user_to_db(self, id):

        try:
            self.cur.execute(f'UPDATE users SET ban = ? WHERE id = ?', ['None', str(id)])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка при разбане пользователя: {e}')
            return False


    def search_ban_user(self, id):
        try:
            req = self.cur.execute('SELECT ban FROM users WHERE id = ?', [str(id)]).fetchone()
            return req
        except Exception as e:
            print(f'ОШибка при поиске айди бана:{e}')


    def add_valute(self, valute, type, min, max, requisite):

        try:
            self.cur.execute('INSERT INTO valute VALUES(?, ?, ?, ?, ?)',
                            [valute, type, min, max, requisite])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка при добавлении валюты: {e}')
            return False


    def give_keyboard_valute(self, type_valute):

        try:
            req = self.cur.execute('SELECT name, type FROM valute WHERE type = ?', [type_valute]).fetchall()
            return req

        except Exception as e:
            print(f'ошибка при выдачи калвиатуры из базы данных: {e}')
            return False

    def give_info_valute(self, name):
        
        try:
            req = self.cur.execute('SELECT requisite FROM valute WHERE name = ?', [name]).fetchall()
            return req

        except Exception as e:
            print(f'Ошибка при выдаче информации о валюте: {e}')
            return False

    def delete_valute(self, name):

        try:
            self.cur.execute('DELETE FROM valute WHERE name = ?', [name])
            self.base.commit()
            return True

        except Exception as e:
            print(f'Ошибка при удалении валюты: {e}')
            return False


    def give_min_and_max(self, name):

        try:
            req = self.cur.execute('SELECT minimal, maximal FROM valute WHERE name = ?', [name]).fetchall()
            return req

        except Exception as e:
            print(f'Ошибка при выдаче минимума и максимума валюты :{e}')
            return False
