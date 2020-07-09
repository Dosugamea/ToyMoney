from pydantic import BaseModel, constr


class ProductModel(BaseModel):
    product_id: int
    product_name: constr(max_length=63)
    product_description: constr(max_length=300)
    product_price: int

    class Config:
        orm_mode = True
