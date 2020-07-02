import csv
from pathlib import Path
import sys
import pandas as pd
from sqlalchemy import create_engine
import chardet
from tqdm import tqdm
import config
from database import *
import shutil
import os

try:
    shutil.rmtree(config.RESULTS_FOLDER)
except FileNotFoundError:
    pass
os.mkdir(config.RESULTS_FOLDER)
init_db()

maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')
        

#Listar arquivos
print("Localizando arquivos...")
csv_files = []
for dir_ in config.FOLDER_WITH_DATABASES.iterdir():
    if dir_.is_file():
        continue
    for entry in dir_.iterdir():
        if not entry.is_file() or not entry.suffix == ".csv":
            continue
        item = {'dbname': entry.parent.name, 'path': entry.absolute()}
        csv_files.append(item)
csv_files.sort(key=lambda x: x['dbname'])

# Analisar os csvs
print("Tentando fazer parsing dos arquivos CSV")
pbar = tqdm(csv_files)

def new_database(name):
    db_obj = DatabaseObj()
    db_obj.name = name
    db_obj.csv_folder = str((config.FOLDER_WITH_DATABASES / name).absolute())
    db_session.add(db_obj)
    db_session.commit()
    return db_obj

db_obj = new_database(csv_files[0]['dbname'])
for item in pbar:
    if item['dbname'] != db_obj.name:
        db_session.commit()
        db_obj = new_database(item['dbname'])
    entry = item['path']
    stat = {}
    csvfile = CsvFile()
    csvfile.database_obj = db_obj
    csvfile.path = str(entry.absolute())
    try:
        with entry.open("r", newline='', encoding=config.CSV_ENCODING) as f:
            reader = csv.reader(fix_nulls(f), delimiter=config.SEPARATOR)
            for i, row in enumerate(reader):
                n = len(row)
                try:
                    stat[n] += 1
                except KeyError:
                    stat[n] = 1    
        csvfile.set_stats_separator(stat)
        n = len(stat.keys())
        if n == 1:
            csvfile.state = "normal"
        else:
            csvfile.state = "separator_problem"
            csvfile.nn_columns = n
    except UnicodeDecodeError:
        csvfile.state = "encoding_problem"
    db_session.add(csvfile)
    pbar.update(1)
db_session.commit()

