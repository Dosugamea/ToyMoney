from pydantic import BaseModel, constr
from datetime import datetime


class TransactionModel(BaseModel):
    transaction_id: int
    transaction_reception: datetime
    transaction_provider: int
    transaction_reciever: int
    transaction_message: constr(max_length=100)

    class Config:
        orm_mode = True
