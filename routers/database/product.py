from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# from setting import ENGINE

Base = declarative_base()


class ProductOrm(Base):
    """
    商品モデル
    """
    __tablename__ = 'products'

    product_id = Column(Integer, autoincrement=True, primary_key=True)
    product_name = Column(String(255))
    product_description = Column(String(255))
    product_price = Column(Integer)

    def __repr__(self):
        return f"<Wallet(id={self.id}, name={self.name}, money={self.money})>"


# Base.metadata.create_all(ENGINE)
