import os


current_directory = os.path.dirname(__file__)
db_file_path= os.path.join(current_directory, "wb_storing.db")

def DBPath():
    return db_file_path