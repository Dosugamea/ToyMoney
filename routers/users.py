from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models


router = APIRouter()


@router.post('/create')
async def create_user(
    user: schemas.UserCreateRequest,
    db: Session = Depends(session)
):
    apiKey = crud.create_user(db, user)
    return {"text": "Created", "apiKey": apiKey}


@router.get('/assets')
async def get_assets(
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    user, inventories = crud.get_user(db, user['id'], True)
    inventories = [
        {
            "id": i[1].id,
            "name": i[1].name,
            "description": i[1].description,
            "price": i[1].price,
            "limit": i[1].inventory_limit,
            "count": i[0].product_count
        }
        for i in inventories
    ]
    return {"text": "ok", "money": user.money, "assets": inventories}


@router.post('/assets/use')
async def use_asset(
    use_request: schemas.ProductUserUseRequest,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    crud.use_product(
        db,
        user["id"],
        use_request.id,
        use_request.amount
    )
    return {"text": "ok"}


@router.get('/money')
async def get_money(
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    user = crud.get_user(db, user['id'], False)
    return {"text": "ok", "money": user.money}


@router.get('/transactions')
async def get_user_transactions(
    page: int = 1,
    sort: int = 1,
    count: int = 20,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    transactions, total = crud.list_transaction(
        db,
        user['id'],
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


@router.post('/transactions/create')
async def create_user_transaction(
    user_transaction: schemas.TransactionUserCreateRequest,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    crud.create_user_transaction(
        db,
        user["id"],
        user_transaction.target_user_id,
        user_transaction.amount
    )
    return {"text": "ok"}


@router.get('/ranking')
async def get_user_ranking(
    page: int = 1,
    sort: int = 5,
    count: int = 20,
    db: Session = Depends(session)
):
    if sort not in [5, 6]:
        sort = 5
    users, total = crud.list_user(
        db,
        page,
        sort,
        count
    )
    users = [
        {
            "id": t.id,
            "name": t.name,
            "money": t.money,
            "is_admin": t.is_admin
        }
        for t in users
    ]
    pages, extra = divmod(total, count)
    if extra:
        pages += 1
    return {
        "text": "ok",
        "users": users,
        "pages": pages,
        "current": page,
        "total": total
    }


@router.get('/admin/list')
async def get_user_account_list(
    page: int = 1,
    sort: int = 1,
    count: int = 20,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    users, total = crud.list_user(
        db,
        page,
        sort,
        count
    )
    users = [
        {
            "id": t.id,
            "name": t.name,
            "money": t.money,
            "is_admin": t.is_admin
        }
        for t in users
    ]
    pages, extra = divmod(total, count)
    if extra:
        pages += 1
    return {
        "text": "ok",
        "users": users,
        "pages": pages,
        "current": page,
        "total": total
    }


@router.get('/admin/{user_id}')
async def get_user_account_as_admin(
    user_id: str,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    user = crud.get_user(db, user_id)
    user = {
        "id": user.id,
        "name": user.name,
        "money": user.money,
        "is_admin": user.is_admin
    }
    return {"text": "ok", "user": user}


@router.put('/admin/{user_id}')
async def put_user_account_as_admin(
    user_id: str,
    user: schemas.UserEditRequest,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.put_user(
        db,
        user_id,
        user.name,
        user.money,
        user.is_admin
    )
    return {"text": "ok"}


@router.delete('/admin/{user_id}')
async def delete_user_account_as_admin(
    user_id: str,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.delete_user(db, user_id)
    return {"text": "ok"}


@router.get('/{user_id}')
async def get_user(
    user_id: str,
    db: Session = Depends(session)
):
    user = crud.get_user(db, user_id)
    user = {
        "id": user.id,
        "name": user.name,
        "money": user.money,
        "is_admin": user.is_admin
    }
    return {"text": "ok", "user": user}
