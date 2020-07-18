from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .authorizator import verify_token, verify_admin
from . import crud, schemas, models


router = APIRouter()


@router.get('/list')
async def get_airdrops(
    page: int = 1,
    sort: int = 1,
    count: int = 20,
    db: Session = Depends(session)
):
    airdrops, total = crud.list_airdrop(db, page, sort, count)
    airdrops = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "amount": p.amount,
            "interval": p.interval
        }
        for p in airdrops
    ]
    pages, extra = divmod(total, count)
    if extra:
        pages += 1
    return {
        "text": "ok",
        "airdrops": airdrops,
        "pages": pages,
        "current": page,
        "total": total
    }


@router.get('/list_with_status')
async def get_airdrop_status(
    page: int = 1,
    sort: int = 1,
    count: int = 20,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    airdrops, total = crud.list_airdrop_with_stat(db, page, sort, count)
    pages, extra = divmod(total, count)
    if extra:
        pages += 1
    return {
        "text": "ok",
        "airdrops": airdrops,
        "pages": pages,
        "current": page,
        "total": total
    }


@router.post('/create')
async def create_airdrop_as_admin(
    airdrop: schemas.AirdropCreateRequest,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.create_airdrop(
        db,
        airdrop.name,
        airdrop.description,
        airdrop.amount,
        airdrop.interval,
        airdrop.mode
    )
    return {"text": "ok"}


@router.get('/{airdrop_id}')
async def get_airdrop(
    airdrop_id: int,
    db: Session = Depends(session)
):
    airdrop = crud.get_airdrop(db, airdrop_id)
    return {
        "text": "ok",
        "id": airdrop.id,
        "name": airdrop.name,
        "description": airdrop.description,
        "amount": airdrop.amount,
        "interval": airdrop.interval,
        "mode": airdrop.mode
    }


@router.put('/{airdrop_id}')
async def set_airdrop_info_as_admin(
    airdrop: schemas.AirdropEditRequest,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.put_airdrop(
        db,
        airdrop.id,
        airdrop.name,
        airdrop.description,
        airdrop.amount,
        airdrop.interval,
        airdrop.mode
    )
    return {"text": "ok"}


@router.delete('/{airdrop_id}')
async def delete_airdrop_as_admin(
    airdrop_id: int,
    admin: dict = Depends(verify_admin),
    db: Session = Depends(session)
):
    crud.delete_airdrop(db, airdrop_id)
    return {"text": "ok"}


@router.post('/{airdrop_id}/claim')
async def claim_airdrop(
    airdrop_id: int,
    user: dict = Depends(verify_token),
    db: Session = Depends(session)
):
    _, before, after = crud.claim_airdrop(db, airdrop_id, user['id'])
    return {"text": "ok", "before": before, "after": after}
