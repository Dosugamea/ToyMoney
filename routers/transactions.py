from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models

router = APIRouter()


@router.get('/')
async def get_transactions_as_admin(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/fee')
async def get_transactions_fee_as_admin(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.put('/fee')
async def set_transactions_fee_as_admin(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}
