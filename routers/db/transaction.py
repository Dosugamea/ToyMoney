from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# from setting import ENGINE

Base = declarative_base()


class Transaction(Base):
    """
    取引モデル
    """
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    provider = Column(Integer)
    reciever = Column(Integer)
    message = Column(String(280))

    def __repr__(self):
        return f"<Transaction(id={self.id}, provider={self.provider}, reciever={self.reciever})>"


# Base.metadata.create_all(ENGINE)
