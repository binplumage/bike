import os
import pandas as pd

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
	sec = 3600 * int(hms[11:13]) + 60 * int(hms[14:16]) + int(hms[17:])
	return sec

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
			start_time = time_to_sce(data[line][1])
			stop_time= time_to_sce(data[line][2])
			start_station_id = data[line][3]
			stop_station_id = data[line][7]
			

set_environment()
main()
