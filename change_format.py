import os
import csv
import pandas as pd
import calendar

#Global variable
# Monday:0, Tuesday:1, ...
weekday_rent = {0 : [0]*24, 1 : [0]*24, 2 : [0]*24, 3 : [0]*24, 4 : [0]*24, 5 : [0]*24, 6 : [0]*24}
weekday_return = {0 : [0]*24, 1 : [0]*24, 2 : [0]*24, 3 : [0]*24, 4 : [0]*24, 5 : [0]*24, 6 : [0]*24}
weekday_count = { x : 0 for x in range(7)}

def make_sure_folder_exists(folder):
    """
    Check if the folder exits, if not then create a folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

def set_environment():
	"""
	Get current working dir and create a result folder.
	"""
	global SCRIPT_DIR, FILE_DIR, RESULT_FOLDER
	SCRIPT_DIR = os.getcwd()
	FILE_DIR = SCRIPT_DIR + "\\data\\"
	RESULT_FOLDER = SCRIPT_DIR + "\\result_data"
	make_sure_folder_exists(RESULT_FOLDER)

def time_to_sce(hms):
	"""
	00:00:00 to 0 sec.
	"""
	sec = 3600 * int(hms[0:2]) + 60 * int(hms[3:5]) + int(hms[6:])
	return sec

def count_weekday_rent_number(year, month, day, sec):
	global weekday_rent
	weekday_rent[calendar.weekday(year, month, day)][sec/3600] += 1

def count_weekday_return_number(year, month, day, sec):
	global weekday_return
	weekday_return[calendar.weekday(year, month, day)][sec/3600] += 1

def get_ymd(time):
	"""
	2014-01-02 00:00:00 to year(2014), month(01), day(02).
	"""
	year = int(time[0:4])
	month = int(time[5:7])
	day = int(time[8:10])

	return year, month, day

def count_weekday_times_in_year(year):
	global weekday_count

	cal = calendar.Calendar()
	for quater in cal.yeardays2calendar(year):
		for month in quater:
			for week in month:
				for day in week:
					if day[0] == 0:
						continue
					else:
						weekday_count[day[1]] += 1

def change_time_format(start_time, stop_time):
	rent_sec = time_to_sce(start_time[11:])
	return_sec = time_to_sce(stop_time[11:])
	rent_year, rent_month, rent_day = get_ymd(start_time)
	return_year, return_month, return_day = get_ymd(stop_time)
	count_weekday_rent_number(rent_year, rent_month, rent_day, rent_sec)
	count_weekday_return_number(return_year, return_month, return_day, return_sec)

def convert_dict_to_df(dic):
	rent_list = []

	for key, value in dic.iteritems():
		tmp_dict = {x : 0 for x in range(24)}
		tmp_dict['weekday'] = key
		tmp_dict['count'] = weekday_count[key]
		for i, nu in enumerate(value):
			tmp_dict[i] = nu
		rent_list.append(tmp_dict)
	df = pd.DataFrame(rent_list, index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
	return df

def write_data_to_csv():
	df_rent = convert_dict_to_df(weekday_rent)
	df_return = convert_dict_to_df(weekday_return)
	df_rent.to_csv("rent.csv", sep=',', encoding='utf-8')
	df_return.to_csv("return.csv", sep=',', encoding='utf-8')

def main():
	#for a_csv in os.listdir(FILE_DIR):
	for a_csv in ['2014_01.csv', '2014_02.csv']:
		df = pd.read_csv(FILE_DIR + a_csv)
		data = df.as_matrix()
		data_number = data.shape[0]
		print data_number
		print "tipduration start_time stop_time start_station_id stop_station_id"

		for line in range(15):
			tipduration = data[line][0]
			change_time_format(data[line][1], data[line][2])
			count_weekday_times_in_year(2014)
			write_data_to_csv()
			#start_time = time_to_sce(data[line][1])
			#stop_time= time_to_sce(data[line][2])
			#start_station_id = data[line][3]
			#stop_station_id = data[line][7]

set_environment()
main()

# test change_time_format function
#change_time_format("2016-05-25 15:37:20" ,"2016-05-27 07:05:01")
