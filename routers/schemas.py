from typing import List
from pydantic import BaseModel, constr
from datetime import datetime


class Product(BaseModel):
    product_id: int
    product_name: constr(max_length=63)
    product_description: constr(max_length=300)
    product_price: int

    class Config:
        orm_mode = True


class Machine(BaseModel):
    id: int
    name: constr(max_length=63)
    description: constr(max_length=300)
    products: List[Product]

    class Config:
        orm_mode = True


class Airdrop(BaseModel):
    id: int
    name: constr(max_length=63)
    description: constr(max_length=300)
    amount: int
    interval: int

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    id: int
    reception: datetime
    provider: int
    reciever: int
    message: constr(max_length=100)

    class Config:
        orm_mode = True


class NewUser(BaseModel):
    name: constr(max_length=20)
    password: constr(min_length=10, max_length=100)

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: constr(max_length=63)
    money: int
    inventories: List[Product]
    is_admin: bool

    class Config:
        orm_mode = True
