from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base

# Database setting
SALT = "UNSAFE_SECRET_KEY"
DB_TYPE = 'sqlite'
USERNAME = ''
PASSWORD = ''
HOST_IP = ''
DB_NAME = 'TOYMONEY'
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
