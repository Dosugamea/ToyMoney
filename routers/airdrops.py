from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('/')
async def get_airdrops():
    return {"text": "hello world!"}


@router.post('/')
async def create_airdrop_as_admin():
    return {"text": "hello world!"}


@router.get('/{airdrop_id}')
async def get_airdrop(airdrop_id: int):
    return {"text": "hello world!"}


@router.put('/{airdrop_id}')
async def set_airdrop_info_as_admin(airdrop_id: int):
    return {"text": "hello world!"}


@router.delete('/{airdrop_id}')
async def delete_airdrop_as_admin(airdrop_id: int):
    return {"text": "hello world!"}


@router.post('/{airdrop_id}/recieve')
async def recieve_airdrop(airdrop_id: int):
    return {"text": "hello world!"}
