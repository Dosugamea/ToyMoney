from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AirdropOrm(Base):
    """
    エアドロップモデル
    """
    __tablename__ = 'airdrops'

    airdrop_id = Column(Integer, primary_key=True)
    airdrop_name = Column(String(63))
    airdrop_description = Column(String(300))
    airdrop_amount = Column(Integer(10))
    airdrop_interval = Column(Integer(10))

    def __repr__(self):
        return f"""<Airdrop(id={self.airdrop_id},
        name={self.airdrop_name},
        description={self.airdrop_description},
        amount={self.airdrop_amount},
        interval={self.airdrop_interval}>"""
