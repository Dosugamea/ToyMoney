from typing import List
from pydantic import BaseModel, constr
from product import ProductModel


class MachineModel(BaseModel):
    machine_id: int
    machine_name: constr(max_length=63)
    machine_description: constr(max_length=300)
    machine_products: List[ProductModel]

    class Config:
        orm_mode = True
