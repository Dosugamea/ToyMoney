from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi import HTTPException
from . import models, schemas
from .authorizator import SALT, generate_token
from hashlib import sha256


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, new_user: schemas.NewUser):
    # 重複するアカウント禁止
    isExist = db.query(models.User.id).filter_by(
        name=new_user.name
    ).scalar() is not None
    if isExist:
        raise HTTPException(
            status_code=400,
            detail="The name is already taken"
        )
    # 新規ユーザー作成
    newUserRequest = models.User(
        name=new_user.name,
        password=sha256((SALT + new_user.password).encode("utf-8")).hexdigest(),
        is_admin=0
    )
    db.add(newUserRequest)
    db.commit()
    # トークン作成
    newUser = db.query(models.User.id).filter_by(
        name=new_user.name
    ).first()
    print(newUser)
    token = generate_token(db, newUser.id)
    return token


def create_product(db: Session, name: str, description: str, price: int):
    pass