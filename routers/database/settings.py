from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Database setting
DB_TYPE = 'sqlite'
USERNAME = ''
PASSWORD = ''
HOST_IP = ''
DB_NAME = 'TOYMONEY'
ECHO = True

if DB_TYPE == 'mysql':
    DATABASE = f'mysql://{USERNAME}:{PASSWORD}@{HOST_IP}/{DB_NAME}?charset=utf8'
else:
    DATABASE = f'sqslite://{DB_NAME}.sqlite3'

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=ECHO
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)
