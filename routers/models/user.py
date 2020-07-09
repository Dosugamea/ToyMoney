from typing import List
from pydantic import BaseModel, constr
from product import ProductModel


class UserModel(BaseModel):
    user_id: int
    user_name: constr(max_length=63)
    user_money: int
    user_inventories: List[ProductModel]
    user_authorization_key: constr(max_length=300)
    user_is_admin: bool

    class Config:
        orm_mode = True
