from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config
import sqlalchemy as sa

engine = create_engine(config.DATABASE_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

class NormalFile(Base):
    __tablename__ = 'normal_file'
    id = sa.Column(sa.Integer, primary_key=True)
    path = sa.Column(sa.Text)


class SeparatorProblemFile(Base):
    __tablename__ = 'separator_problem_file'
    id = sa.Column(sa.Integer, primary_key=True)
    path = sa.Column(sa.Text)
    n = sa.Column(sa.Integer)


class EncodingProblemFile(Base):
    __tablename__ = 'encoding_problem_file'
    id = sa.Column(sa.Integer, primary_key=True)
    path = sa.Column(sa.Text)
    encoding = sa.Column(sa.String(50))
    confidence = sa.Column(sa.Float)
    language = sa.Column(sa.String(50))


def init_db():
    metadata = MetaData(engine)
    Base.metadata.create_all(bind=engine)
