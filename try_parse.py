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
        csv_files.append(entry.absolute())

# Analisar os csvs
print("Tentando fazer parsing dos arquivos CSV")
pbar = tqdm(csv_files)
for entry in pbar:
    stat = {}
    try:
        with entry.open("r", newline='', encoding=config.CSV_ENCODING) as csvfile:
            reader = csv.reader(fix_nulls(csvfile), delimiter=",")
            for i, row in enumerate(reader):
                n = len(row)
                try:
                    stat[n] += 1
                except KeyError:
                    stat[n] = 1
        # stats[entry.name]= stat
        n = len(stat.keys())
        if n == 1:
            file_ = NormalFile()
        else:
            file_ = SeparatorProblemFile()
            file_.n = n
    except UnicodeDecodeError:
        file_ = EncodingProblemFile()
    file_.path =  str(entry.absolute())
    db_session.add(file_)
    pbar.update(1)
db_session.commit()

