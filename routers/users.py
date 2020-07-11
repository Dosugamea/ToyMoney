from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models

router = APIRouter()


@router.post('/create')
async def create_user(
    new_user: schemas.NewUser,
    db: Session = Depends(session)
):
    apiKey = crud.create_user(db, new_user)
    return {"text": "Created", "apiKey": apiKey}


@router.get('/secret')
async def secret_space(
    user: dict = Depends(verify_token)
):
    return {"text": "Authorization succeed!", "data": user}


@router.get('/assets')
async def get_assets(
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/transactions')
async def get_user_transactions(
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.post('/transactions/create')
async def create_user_transaction(
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/ranking')
async def get_user_ranking(
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/admin/list')
async def get_user_account_list(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/admin/{account_id}')
async def get_user_account_as_admin(
    account_id: str,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.put('/admin/{account_id}')
async def put_user_account_as_admin(
    account_id: str,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.delete('/admin/{account_id}')
async def delete_user_account_as_admin(
    account_id: str,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


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
