from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('/')
async def get_transactions_as_admin():
    return {"text": "hello world!"}


@router.get('/fee')
async def get_transactions_fee_as_admin():
    return {"text": "hello world!"}


@router.put('/fee')
async def set_transactions_fee_as_admin():
    return {"text": "hello world!"}
