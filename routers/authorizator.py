from itsdangerous import JSONWebSignatureSerializer as Serializer
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import session
from .models import User


SALT = "UNSAFE_SECRET_KEY"
token_serializer = Serializer(SALT)


def generate_token(db: Session, id: str):
    targetUser = db.query(User).filter(User.id == id).first()
    token = token_serializer.dumps({
        'id': id,
        'seq': targetUser.authorization_seq + 1,
        'is_admin': 0
    }).decode('utf-8')
    targetUser.authorization_key = token
    targetUser.authorization_seq += 1
    db.commit()
    return token


async def verify_token(
    db: Session = Depends(session),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header was not presented"
        )
    try:
        userData = token_serializer.loads(authorization.split("Bearer ")[1])
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization"
        )
    if 'id' not in userData:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization"
        )
    isExist = db.query(User).filter_by(
        id=userData['id'],
        authorization_seq=userData['seq'],
        is_admin=userData['is_admin']
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization"
        )
    return userData


async def verify_admin(
    db: Session = Depends(session),
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header was not presented"
        )
    try:
        userData = token_serializer.loads(authorization.split("Bearer ")[1])
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization"
        )
    if 'id' not in userData:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization"
        )
    isExist = db.query(User).filter_by(
        id=userData['id'],
        authorization_seq=userData['seq'],
        is_admin=userData['is_admin']
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization"
        )
    if not userData["is_admin"]:
        raise HTTPException(
            status_code=401,
            detail="You are not admin"
        )
    return userData
