from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class MachineOrm(Base):
    """
    自販機モデル
    """
    __tablename__ = 'machines'

    machine_id = Column(Integer, primary_key=True)
    machine_name = Column(String(63))
    machine_description = Column(String(300))
    machine_products = relationship("Product", backref="machines")

    def __repr__(self):
        return f"""<Machine(
        id={self.machine_id},
        name={self.machine_name},
        description={self.machine_description}),
        products={self.machine_products})>"""
