from datetime import date
import datetime


def all_stat(db_list):

	name_staff = []

	for log in db_list:

		name_staff.append(log[2])

	clear_name_staff = list(set(name_staff))

	text_return = '➕ Профит: '

	for name in clear_name_staff:



		all_profit = 0

		for log in db_list:
			amount = log[0]

			data = log[3].split('-')

			if name == log[2]:

				all_profit += float(amount)

			else:
				pass

		text_return += f'''
{name}: {all_profit}'''		
		

	return text_return



def custom_stat_func(db_list, time):

	dt_now = f'{str(date.today())}-{datetime.datetime.today().isocalendar()[1]}'.split('-')

	name_staff = []

	for log in db_list:

		name_staff.append(log[2])

	clear_name_staff = list(set(name_staff))

	text_return = ''

	if time == 'week':
		text_return += '➕За неделю:'
		for name in clear_name_staff:

			week = 0
			day = 0
			month = 0

			for log in db_list:
				amount = log[0]

				data = log[3].split('-')

				if name == log[2]:

					if str(data[3]) == dt_now[3]:

						week += float(amount)
					else:
						pass

				else:
					pass

			text_return += f'''
	{name}: {week}'''		


		return text_return

	elif time == 'day':
		text_return += f'➕За день:'
		for name in clear_name_staff:
			day = 0			
			for log in db_list:
				amount = log[0]

				data = log[3].split('-')

				if name == log[2]:

					if str(data[2]) == dt_now[2]:

						day += float(amount)
					else:
						pass

				else:
					pass

			text_return += f'''
	{name}: {day}'''		

		return text_return

	elif time == 'month':
		text_return += f'➕За месяц:'
		for name in clear_name_staff:
			month = 0			
			for log in db_list:
				amount = log[0]

				data = log[3].split('-')

				if name == log[2]:

					if str(data[1]) == dt_now[1]:

						month += float(amount)
					else:
						pass

				else:
					pass

			text_return += f'''
	{name}: {month}'''		

		return text_return