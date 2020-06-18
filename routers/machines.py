from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('/')
async def get_machines():
    return {"text": "hello world!"}


@router.post('/')
async def create_machine_as_admin():
    return {"text": "hello world!"}


@router.get('/{machine_id}')
async def get_machine(machine_id: int):
    return {"text": "hello world!"}


@router.put('/{machine_id}')
async def set_machine_info_as_admin(machine_id: int):
    return {"text": "hello world!"}


@router.delete('/{machine_id}')
async def delete_machine_as_admin(machine_id: int):
    return {"text": "hello world!"}


@router.post('/{machine_id}/{product_id}/buy')
async def buy_product_from_machine(machine_id: int, product_id: int):
    return {"text": "hello world!"}
