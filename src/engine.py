from sqlalchemy.engine.base import Engine
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base


engine: Engine = None
DBSession = sessionmaker(bind=engine)


def init_db(file: str):
    engine = create_engine(url=file)
    Base.metadata.bind = engine
    DBSession.bind = engine
