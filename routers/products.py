from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('/')
async def get_products():
    return {"text": "hello world!"}


@router.post('/')
async def create_product_as_admin():
    return {"text": "hello world!"}


@router.get('/{product_id}')
async def get_product(product_id: int):
    return {"text": "hello world!"}


@router.put('/{product_id}')
async def set_product_info_as_admin(product_id: int):
    return {"text": "hello world!"}


@router.delete('/{product_id}')
async def delete_product_as_admin(product_id: int):
    return {"text": "hello world!"}
