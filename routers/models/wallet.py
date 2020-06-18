from pydantic import BaseModel, constr


class WalletModel(BaseModel):
    id: int
    money: int
    name: constr(max_length=63)

    class Config:
        orm_mode = True
