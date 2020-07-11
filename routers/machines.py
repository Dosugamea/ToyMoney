from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models


router = APIRouter()


@router.get('/list')
async def get_machines(
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/{machine_id}')
async def get_machine(
    machine_id: int,
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.post('/create')
async def create_machine_as_admin(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.put('/{machine_id}')
async def set_machine_info_as_admin(
    machine_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.delete('/{machine_id}')
async def delete_machine_as_admin(
    machine_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.post('/{machine_id}/{product_id}/buy')
async def buy_product_from_machine(
    machine_id: int,
    product_id: int,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}
