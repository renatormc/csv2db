from pathlib import Path
import os

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))


CSV_ENCODING = "ISO-8859-1"
RESULTS_FOLDER = Path('results')
SQLITE_PATH = RESULTS_FOLDER / "stat.db"
DATABASE_URL = f"sqlite:///{SQLITE_PATH}"
FOLDER_WITH_DATABASES =  Path(r'E:\O18 - copy\FINANCEIRO E CONTABILIDADE')
DESTINATION_FOLDER = Path(r'E:\O18 - copy\Bancos Convertidos')
CHUNCK_SIZE_ENCODING_CHECK = 5000
SEPARATOR = ","
CHUNKSIZE_READ_CSV = 10**6
