import os

def make_sure_folder_exists(folder):
    """
    Check if the folder exits, if not then create a folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

def set_environment():
    SCRIPT_DIR = os.getcwd()
    RESULT_FOLDER = SCRIPT_DIR + "\\result_data"
    make_sure_folder_exists(RESULT_FOLDER)


set_environment()
