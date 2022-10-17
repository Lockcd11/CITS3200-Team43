from neo4j import GraphDatabase
import os
from fileGrab import get_import_file_location
import shutil

def clear_db_file(location):
    folder = get_import_file_location() + location
    filename = [f for f in os.listdir(folder) if '.csv' in f.lower()]
    for file in filename:
        file_path = os.path.join(folder, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return 1

def move_csvs(location):
    filename = [f for f in os.listdir('app\\static\\pythonScripts\\current_csvs' + location) if '.csv' in f.lower()]
    for file in filename:
        file_path = os.path.join('app\\static\\pythonScripts\\current_csvs' + location, file)
        new_path = get_import_file_location() + location + file
        shutil.copyfile('app\\static\\pythonScripts\\current_csvs' + location + file, new_path)
        
def transfer_csvs(files):
    if files == 1:
        clear_db_file('')
        move_csvs('\\')
    elif files == 2:
        clear_db_file('\\add')
        move_csvs('\\add\\')