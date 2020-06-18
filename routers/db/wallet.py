from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from setting import ENGINE

Base = declarative_base()


class Wallet(Base):
    """
    ユーザーモデル
    """
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    money = Column(Integer)

    def __repr__(self):
        return f"<Wallet(id={self.id}, name={self.name}, money={self.money})>"


Base.metadata.create_all(ENGINE)
