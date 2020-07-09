from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('/')
async def get_user_wallet():
    return {"text": "hello world!"}


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
