from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models


router = APIRouter()


@router.get('/list')
async def get_airdrops(
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/{airdrop_id}')
async def get_airdrop(
    airdrop_id: int,
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.post('/create')
async def create_airdrop_as_admin(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.put('/{airdrop_id}')
async def set_airdrop_info_as_admin(
    airdrop_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.delete('/{airdrop_id}')
async def delete_airdrop_as_admin(
    airdrop_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.post('/{airdrop_id}/claim')
async def recieve_airdrop(
    airdrop_id: int,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}
