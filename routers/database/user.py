from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserOrm(Base):
    """
    ユーザーモデル
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255))
    user_inventories = relationship("Product", backref="users")
    user_authorization_key = Column(String(255))
    user_is_admin = Column(Integer(1))

    def __repr__(self):
        return f"""<User(id={self.user_id},
        name={self.user_name},
        is_admin={self.user_is_admin}),
        inventories={self.user_inventories},
        key={self.user_authorization_key})>"""
