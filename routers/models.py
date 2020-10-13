from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DATETIME
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# SQLalchemy Models

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
    inventory_limit = Column(Integer)

    def __repr__(self):
        return f"""<Product(id={self.id},
        name={self.name},
        description={self.description},
        price={self.price}),
        inventory_limit={self.inventory_limit}>"""


class UserInventory(Base):
    """
    ユーザーインベントリモデル
    """
    __tablename__ = 'user_inventories'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    product_count = Column(Integer)

    def __repr__(self):
        return f"<UserInventory(owner={self.user_id}, product={self.product_id}, count={self.product_count})>"


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
    mode = Column(Integer)

    def __repr__(self):
        return f"""<Airdrop(id={self.id},
        name={self.name},
        description={self.description},
        amount={self.amount},
        mode={self.mode},
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

    provider_type 0: ユーザー 1: エアドロップ 2: 商品 3: 強制
    receiver_type 0: ユーザー 1: エアドロップ 2: 商品 3: 強制 4: 使用
    """
    __tablename__ = 'transactions'

    id = Column(Integer, autoincrement=True, primary_key=True)
    reception = Column(
        DATETIME,
        default=datetime.now,
        nullable=False
    )
    provider_type = Column(Integer)
    provider = Column(Integer)
    receiver_type = Column(Integer)
    receiver = Column(Integer)
    amount = Column(Integer)
    message = Column(String(280))

    def __repr__(self):
        return f"""<Transaction(
        id={self.id},
        reception={self.reception.strftime('%Y-%m-%d %H:%M:%S')},
        provider_type={self.provider_type},
        provider={self.provider},
        receiver_type={self.receiver_type},
        receiver={self.receiver},
        amount={self.amount},
        message={self.message})>"""


class User(Base):
    """
    ユーザーモデル
    """
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255))
    money = Column(Integer, server_default="0")
    password = Column(String(300))
    inventories = relationship("UserInventory")
    authorization_key = Column(String(255))
    authorization_seq = Column(Integer, server_default="0")
    is_admin = Column(Integer, server_default="0")

    def __repr__(self):
        return f"""<User(id={self.id},
        name={self.name},
        inventories={self.inventories},
        authorization_key={self.authorization_key},
        authorization_seq={self.authorization_seq},
        is_admin={self.is_admin})>"""
