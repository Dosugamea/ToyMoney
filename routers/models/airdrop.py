from pydantic import BaseModel, constr


class AirdropModel(BaseModel):
    airdrop_id: int
    airdrop_name: constr(max_length=63)
    airdrop_description: constr(max_length=300)
    airdrop_amount: int
    airdrop_interval: int

    class Config:
        orm_mode = True
