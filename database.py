from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config
import sqlalchemy as sa
from sqlalchemy.orm import relationship
import json


engine = create_engine(config.DATABASE_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

class DatabaseObj(Base):
    __tablename__ = 'database'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))
    csv_folder = sa.Column(sa.Text)
    files = relationship("CsvFile", backref="database_obj")


class CsvFile(Base):
    __tablename__ = 'csvfile'
    id = sa.Column(sa.Integer, primary_key=True)
    state = sa.Column(sa.String(50))
    path = sa.Column(sa.Text)
    encoding = sa.Column(sa.String(50))
    confidence = sa.Column(sa.Float)
    language = sa.Column(sa.String(50))
    nn_columns = sa.Column(sa.Integer)
    stats_separator = sa.Column(sa.Text)
    database_obj_id = sa.Column(sa.Integer, sa.ForeignKey("database.id"))

    def set_stats_separator(self, value):
        self.stats_separator = json.dumps(value)



def init_db():
    metadata = MetaData(engine)
    Base.metadata.create_all(bind=engine)
