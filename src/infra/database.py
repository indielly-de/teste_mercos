from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from infra.settings import settings

engine = create_engine(str(settings.DATABASE_URL))

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def init_database():
    Base.metadata.create_all(bind=engine)


def get_database():
    db = Session()
    try:
        yield db
    finally:
        db.close()
