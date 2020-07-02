from database import *
from tqdm import tqdm
import chardet
from pathlib import Path


print("Detectando encoding dos arquivos com erro de encoding")
pbar = tqdm(db_session.query(EncodingProblemFile).all())
for file_ in pbar:
    path = Path(file_.path)
    with path.open("rb") as f:
        data = f.read(config.CHUNCK_SIZE_ENCODING_CHECK)
        res = chardet.detect(data)
    file_.encoding = res['encoding']
    file_.confidence = res['confidence']
    file_.language = res['language']
    db_session.add(file_)
    pbar.update(1)
db_session.commit()
print("Finalizou")