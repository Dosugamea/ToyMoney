from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Product(Base):
    """
    商品モデル
    """
    __tablename__ = 'products'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    price = Column(Integer)

    def __repr__(self):
        return f"<Wallet(id={self.id}, name={self.name}, money={self.money})>"


class UserInventory(Base):
    """
    ユーザーインベントリモデル
    """
    __tablename__ = 'user_inventories'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)

    def __repr__(self):
        return f"<UserInventory(owner={self.user_id}, product={self.product_id})>"


class MachineInventory(Base):
    """
    自販機インベントリモデル
    """
    __tablename__ = 'machine_inventories'

    machine_id = Column(Integer, ForeignKey('machines.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)

    def __repr__(self):
        return f"<MachineInventory(owner={self.machine_id}, product={self.product_id})>"


class Airdrop(Base):
    """
    エアドロップモデル
    """
    __tablename__ = 'airdrops'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(63))
    description = Column(String(300))
    amount = Column(Integer)
    interval = Column(Integer)

    def __repr__(self):
        return f"""<Airdrop(id={self.id},
        name={self.name},
        description={self.description},
        amount={self.amount},
        interval={self.interval}>"""


class Machine(Base):
    """
    自販機モデル
    """
    __tablename__ = 'machines'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(63))
    description = Column(String(300))
    products = relationship("MachineInventory")

    def __repr__(self):
        return f"""<Machine(
        id={self.id},
        name={self.name},
        description={self.description}),
        products={self.products})>"""


class Transaction(Base):
    """
    取引モデル
    """
    __tablename__ = 'transactions'

    id = Column(Integer, autoincrement=True, primary_key=True)
    reception = Column(
        DATETIME,
        default=datetime.now,
        nullable=False
    )
    provider = Column(Integer, ForeignKey('users.id'))
    reciever = Column(Integer, ForeignKey('users.id'))
    message = Column(String(280))

    def __repr__(self):
        return f"""<Transaction(
        id={self.id},
        reception={self.reception.strftime('%Y-%m-%d %H:%M:%S')},
        provider={self.provider},
        reciever={self.reciever}),
        message={self.message}>"""


class User(Base):
    """
    ユーザーモデル
    """
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    inventories = relationship("UserInventory")
    authorization_key = Column(String(255))
    is_admin = Column(Integer, server_default="0")

    def __repr__(self):
        return f"""<User(id={self.id},
        name={self.name},
        inventories={self.inventories},
        authorization_key={self.authorization_key},
        is_admin={self.is_admin})>"""
