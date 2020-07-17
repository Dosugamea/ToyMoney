from typing import List, Optional
from pydantic import BaseModel, constr
from datetime import datetime


class Product(BaseModel):
    id: int
    name: constr(max_length=63)
    description: constr(max_length=300)
    price: int

    class Config:
        orm_mode = True


class ProductCreateRequest(BaseModel):
    name: constr(max_length=63)
    description: constr(max_length=300)
    price: int

    class Config:
        orm_mode = True


class ProductEditRequest(BaseModel):
    name: Optional[str] = constr(max_length=63)
    description: Optional[str] = constr(max_length=300)
    price: Optional[int] = -1

    class Config:
        orm_mode = True


class Machine(BaseModel):
    id: int
    name: constr(max_length=63)
    description: constr(max_length=300)
    products: List[Product]

    class Config:
        orm_mode = True


class MachineCreateRequest(BaseModel):
    name: constr(max_length=63)
    description: constr(max_length=300)
    products: List[int]

    class Config:
        orm_mode = True


class MachineEditRequest(BaseModel):
    name: Optional[str] = constr(max_length=63)
    description: Optional[str] = constr(max_length=300)
    products:  Optional[List[Product]] = []

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


class AirdropCreateRequest(BaseModel):
    name: constr(max_length=63)
    description: constr(max_length=300)
    amount: int
    interval: int

    class Config:
        orm_mode = True


class AirdropEditRequest(BaseModel):
    name: Optional[str] = constr(max_length=63)
    description: Optional[str] = constr(max_length=300)
    amount: Optional[int] = -1
    interval: Optional[int] = -1

    class Config:
        orm_mode = True


class Transaction(BaseModel):
    id: int
    reception: datetime
    provider: int
    reciever: int
    amount: int
    message: constr(max_length=100)

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


class UserCreateRequest(BaseModel):
    name: constr(max_length=20)
    password: constr(min_length=10, max_length=100)

    class Config:
        orm_mode = True


class UserEditRequest(BaseModel):
    name: Optional[str] = None
    money: Optional[int] = None
    is_admin: Optional[bool] = None

    class Config:
        orm_mode = True
