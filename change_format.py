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

def main():
	#for a_csv in os.listdir(FILE_DIR):
	for a_csv in ['2014_01.csv', '2014_02.csv']:
		data = pd.read_csv(FILE_DIR + a_csv)
		print data.head()

set_environment()
main()
