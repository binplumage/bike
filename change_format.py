import os
import csv
import pandas as pd
import calendar
import datetime

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

def make_sure_file_exists(filename):
	if os.path.isfile(filename):
		NOW_TIME = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
		os.rename(filename, filename + "_" + NOW_TIME)

def set_environment():
	"""
	Get current working dir and create a result folder.
	"""
	global SCRIPT_DIR, FILE_DIR, RESULT_FOLDER
	SCRIPT_DIR = os.getcwd()
	FILE_DIR = SCRIPT_DIR + "\\data\\"
	RESULT_FOLDER = SCRIPT_DIR + "\\result_data"
	make_sure_folder_exists(RESULT_FOLDER)
	make_sure_file_exists(RESULT_FOLDER + "\\rent.csv")
	make_sure_file_exists(RESULT_FOLDER + "\\return.csv")

def time_to_sce(hms):
	"""
	00:00:00 to 0 sec.
	"""
	sec = 3600 * int(hms[0:2]) + 60 * int(hms[3:5]) + int(hms[6:])
	return sec

def count_weekday_rent_number(year, month, day, sec):
	global weekday_rent
	if year == 2014:
		weekday_rent[calendar.weekday(year, month, day)][sec/3600] += 1

def count_weekday_return_number(year, month, day, sec):
	global weekday_return
	if year == 2014:
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
		#tmp_dict['count'] = weekday_count[key]
		for i, nu in enumerate(value):
			tmp_dict[i] = float(nu/weekday_count[key])
		rent_list.append(tmp_dict)
	df = pd.DataFrame(rent_list, index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
	return df

def write_data_to_csv():
	df_rent = convert_dict_to_df(weekday_rent)
	df_return = convert_dict_to_df(weekday_return)
	df_rent.to_csv( RESULT_FOLDER +"\\rent.csv", sep=',', encoding='utf-8')
	df_return.to_csv( RESULT_FOLDER + "\\return.csv", sep=',', encoding='utf-8')

def convert_time_format(time):

	output_time = datetime.datetime.strptime(time,"%m/%d/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

	return output_time

def main():
	csv_file = os.listdir(FILE_DIR)
	file_2014 = filter(lambda x:'2014' in x, csv_file)
	for a_csv in file_2014:
		file_month = a_csv[5:7]
		df = pd.read_csv(FILE_DIR + a_csv)
		data = df.as_matrix()
		data_number = data.shape[0]

		for line in range(data_number):
			tipduration = data[line][0]
			start_time = data[line][1]
			stop_time = data[line][2]
			if int(file_month) >= 9:
				start_time = convert_time_format(start_time)
				stop_time = convert_time_format(stop_time)
			change_time_format(start_time, stop_time)
	count_weekday_times_in_year(2014)
	write_data_to_csv()
			#start_station_id = data[line][3]
			#stop_station_id = data[line][7]

print datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
print "Start"
set_environment()
main()
print datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
print "End"

# test change_time_format function
#change_time_format("2016-05-25 15:37:20" ,"2016-05-27 07:05:01")
