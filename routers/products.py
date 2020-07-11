from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models


router = APIRouter()


@router.get('/list')
async def get_products(
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.post('/create')
async def create_product_as_admin(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/{product_id}')
async def get_product(
    product_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.put('/{product_id}')
async def set_product_info_as_admin(
    product_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.delete('/{product_id}')
async def delete_product_as_admin(
    product_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}
