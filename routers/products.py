from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models


router = APIRouter()


@router.get('/list')
async def get_products(
    page: int = 1,
    sort: int = 1,
    count: int = 20,
    db: Session = Depends(session)
):
    products, total = crud.list_product(db, page, sort, count)
    products = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price
        }
        for p in products
    ]
    pages, extra = divmod(total, count)
    if extra:
        pages += 1
    return {
        "text": "ok",
        "products": products,
        "pages": pages,
        "current": page,
        "total": total
    }


@router.post('/create')
async def create_product_as_admin(
    product: schemas.ProductCreateRequest,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.create_product(
        db,
        product.name,
        product.description,
        product.price
    )
    return {"text": "ok"}


@router.get('/{product_id}')
async def get_product(
    product_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    product = crud.get_product(
        db,
        product_id
    )
    return {
        "text": "ok",
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price
    }


@router.put('/{product_id}')
async def set_product_info_as_admin(
    product: schemas.ProductEditRequest,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.put_product(
        db,
        product.id,
        product.name,
        product.description,
        product.price
    )
    return {"text": "ok"}


@router.delete('/{product_id}')
async def delete_product_as_admin(
    product_id: int,
    user: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.delete_product(db, product_id)
    return {"text": "ok"}


@router.post('/{product_id}/buy')
async def buy_product(
    product_id: int,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    crud.buy_product(db, user['id'], product_id)
    return {"text": "ok"}
