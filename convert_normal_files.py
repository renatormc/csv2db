import config
from database import *
import pandas as pd 
import shutil
import os
from sqlalchemy import create_engine
from pathlib import Path
from tqdm import tqdm

try:
    shutil.rmtree(config.DESTINATION_FOLDER)
except FileNotFoundError:
    pass
os.mkdir(config.DESTINATION_FOLDER)


totalfiles = db_session.query(CsvFile).filter(CsvFile.state == 'normal').count()
with tqdm(total=totalfiles) as pbar:
    for db in db_session.query(DatabaseObj).all():
        database_file = config.DESTINATION_FOLDER / f"{db.name}.db"
        engine = create_engine(f"sqlite:///{database_file}", echo=False)
        csvfiles = db_session.query(CsvFile).filter(CsvFile.database_obj == db, CsvFile.state == 'normal').all()
        for csvfile in csvfiles:
            for chunk in pd.read_csv(csvfile.path, chunksize=config.CHUNKSIZE_READ_CSV):
                tablename = Path(csvfile.path).stem
                chunk.to_sql(tablename, con=engine, if_exists="append")
            pbar.update(1)
        

