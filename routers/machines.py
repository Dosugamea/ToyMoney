from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models


router = APIRouter()


@router.get('/list')
async def get_machines(
    page: int = 1,
    sort: int = 1,
    count: int = 20,
    db: Session = Depends(session)
):
    machines, total = crud.list_machine(db, page, sort, count)
    machines = [
        {
            "id": m.id,
            "name": m.name,
            "description": m.description,
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "price": p.price
                }
                for p in m.products
            ]
        }
        for m in machines
    ]
    pages, extra = divmod(total, count)
    if extra:
        pages += 1
    return {
        "text": "ok",
        "machines": machines,
        "pages": pages,
        "current": page,
        "total": total
    }


@router.post('/create')
async def create_machine_as_admin(
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    return {"text": "hello world!"}


@router.get('/{machine_id}')
async def get_machine(
    machine_id: int,
    db: Session = Depends(session)
):
    machine = crud.get_machine(
        db,
        machine_id
    )
    return {
        "text": "ok",
        "id": machine.id,
        "name": machine.name,
        "description": machine.description,
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price
            }
            for p in machine.products
        ]
    }


@router.put('/{machine_id}')
async def set_machine_info_as_admin(
    machine: schemas.MachineEditRequest,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.put_machine(
        db,
        machine.id,
        machine.name,
        machine.description,
        machine.products
    )
    return {"text": "ok"}


@router.delete('/{machine_id}')
async def delete_machine_as_admin(
    machine_id: int,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.delete_machine(db, machine_id)
    return {"text": "ok"}


@router.post('/{machine_id}/{product_id}/buy')
async def buy_product_from_machine(
    machine_id: int,
    product_id: int,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    crud.buy_product(db, user['id'], product_id)
    return {"text": "ok"}
