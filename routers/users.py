from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from . import crud, schemas

router = APIRouter()


@router.get('/{user_id}', response_model=schemas.User)
async def get_user(user_id: str, db: Session = Depends(session)):
    """
    ユーザー情報を取得します
    :param user_id: UserID
    :param db: DB Session
    :return: User Profile
    :rtype: JSON
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found: {user_id}")
    return user


@router.post('/create')
async def create_user_wallet():
    return {"text": "hello world!"}


@router.get('/property')
async def get_user_property():
    return {"text": "hello world!"}


@router.get('/transactions')
async def get_user_transactions():
    return {"text": "hello world!"}


@router.post('/transactions/create')
async def create_user_transaction():
    return {"text": "hello world!"}


@router.get('/ranking')
async def get_user_ranking():
    return {"text": "hello world!"}


@router.get('/list')
async def get_user_wallet_list():
    return {"text": "hello world!"}


@router.get('/{wallet_id}')
async def get_user_wallet_as_admin():
    return {"text": "hello world!"}


@router.put('/{wallet_id}')
async def put_user_wallet_as_admin():
    return {"text": "hello world!"}


@router.delete('/{wallet_id}')
async def delete_user_wallet_as_admin():
    return {"text": "hello world!"}
