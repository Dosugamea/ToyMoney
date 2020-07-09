from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class TransactionOrm(Base):
    """
    取引モデル
    """
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, autoincrement=True, primary_key=True)
    transaction_reception = Column(DATETIME, default=datetime.now, nullable=False)
    transaction_provider = Column(Integer, ForeignKey('user.user_id'))
    transaction_reciever = Column(Integer, ForeignKey('user.user_id'))
    transaction_message = Column(String(280))

    def __repr__(self):
        return f"""<Transaction(
        id={self.transaction_id},
        reception={self.transaction_reception.strftime('%Y-%m-%d %H:%M:%S')},
        provider={self.transaction_provider},
        reciever={self.transaction_reciever}),
        message={self.transaction_message}>"""
