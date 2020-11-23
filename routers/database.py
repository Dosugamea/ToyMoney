from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base
from os import environ
from dotenv import load_dotenv
load_dotenv(verbose=True, override=True)

# Database setting
SALT = environ.get("SALT")
DB_TYPE = environ.get("DB_TYPE")
USERNAME = environ.get("DB_USER")
PASSWORD = environ.get("DB_PASS")
HOST_IP = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")
ECHO = False

if DB_TYPE == 'mysql':
    DATABASE = f'mysql://{USERNAME}:{PASSWORD}@{HOST_IP}/{DB_NAME}?charset=utf8'
    engine = create_engine(
        DATABASE,
        encoding="utf-8",
        echo=ECHO
    )
else:
    DATABASE = f'sqlite:///{DB_NAME}.sqlite3'
    engine = create_engine(
        DATABASE,
        encoding="utf-8",
        connect_args={"check_same_thread": False},
        echo=ECHO
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def session():
    """
    Get Database Session
    :return:
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
