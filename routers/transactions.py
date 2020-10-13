from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models

router = APIRouter()


@router.get('/')
async def get_transactions_as_admin(
    page: int = 1,
    sort: int = 1,
    count: int = 20,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    transactions, total = crud.list_transaction_as_admin(
        db,
        page,
        sort,
        count
    )
    transactions = [
        {
            "id": t.id,
            "amount": t.amount,
            "reception": t.reception,
            "provider_type": t.provider_type,
            "provider": t.provider,
            "receiver_type": t.receiver_type,
            "receiver": t.receiver,
        }
        for t in transactions
    ]
    pages, extra = divmod(total, count)
    if extra:
        pages += 1
    return {
        "text": "ok",
        "transactions": transactions,
        "pages": pages,
        "current": page,
        "total": total
    }
