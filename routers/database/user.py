from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserOrm(Base):
    """
    ユーザーモデル
    """
    __tablename__ = 'users'

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(255))
    user_inventories = relationship("Product", backref="users")
    user_authorization_key = Column(String(255))
    user_is_admin = Column(Integer(1), server_default="0")

    def __repr__(self):
        return f"""<User(id={self.user_id},
        name={self.user_name},
        inventories={self.user_inventories},
        authorization_key={self.user_authorization_key},
        is_admin={self.user_is_admin})>"""