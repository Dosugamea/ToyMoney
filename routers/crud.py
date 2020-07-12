from sqlalchemy.orm import Session
from sqlalchemy.sql import text, desc, asc, or_
from fastapi import HTTPException
from typing import List
from . import models, schemas
from .authorizator import SALT, generate_token
from hashlib import sha256


def list_user(db: Session, page: int, sort: int, count: int):
    q = db.query(models.User)
    sortDict = {
        1: desc(models.User.id),
        2: asc(models.User.id),
        3: desc(models.User.name),
        4: asc(models.User.name),
        5: desc(models.User.money),
        6: asc(models.User.money)
    }
    if sort > 6:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset(page*count).all()
    return q


def create_user(db: Session, new_user: schemas.NewUser):
    # 重複するアカウント禁止
    isExist = db.query(models.User.id).filter_by(
        name=new_user.name
    ).scalar() is not None
    if isExist:
        raise HTTPException(
            status_code=400,
            detail="The user name is already taken"
        )
    # 新規ユーザー作成
    newUserRequest = models.User(
        name=new_user.name,
        password=sha256(
            (SALT + new_user.password).encode("utf-8")
        ).hexdigest(),
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


def get_user(db: Session, user_id: int):
    isExist = db.query(models.User.id).filter_by(
        id=user_id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The user is not exist"
        )
    return db.query(models.User).filter(models.User.id == user_id).first()


def put_user(
    db: Session,
    user_id: int,
    name: str = '',
    money: int = None,
    is_admin: int = None
):
    # パラメータ確認
    if not name and money is None and is_admin is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid request"
        )
    isExist = db.query(models.User.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The user is not exist"
        )
    # アップデート
    user_update = db.query(models.User).filter(
        models.User.id == id
    ).first()
    if name:
        user_update.name = name
    if money is not None:
        user_update.money = money
    if is_admin is not None:
        user_update.is_admin = is_admin
    db.commit()
    return True


def delete_user(db: Session, id: int):
    isExist = db.query(models.User.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The user is not exist"
        )
    db.query(models.User).filter(
        models.User.id == id
    ).delete()
    # TODO: Replace transactions as deleted-user account
    db.query(models.Transaction).filter(
        or_(
            models.Transaction.provider == id,
            models.Transaction.reciever == id
        )
    ).delete()
    db.commit()
    return True


def list_product(db: Session, page: int, sort: int, count: int):
    q = db.query(models.Product)
    sortDict = {
        1: desc(models.Product.id),
        2: asc(models.Product.id),
        3: desc(models.Product.name),
        4: asc(models.Product.name),
        5: desc(models.Product.price),
        6: asc(models.Product.price)
    }
    if sort > 6:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset(page*count).all()
    return q


def create_product(db: Session, name: str, description: str, price: int):
    isExist = db.query(models.Product.id).filter_by(
        name=name
    ).scalar() is not None
    if isExist:
        raise HTTPException(
            status_code=400,
            detail="The product name is already used"
        )
    newProductRequest = models.Product(
        name=name,
        description=description,
        price=price
    )
    db.add(newProductRequest)
    db.commit()
    return True


def get_product(db: Session, id: int):
    isExist = db.query(models.Product.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The product is not exist"
        )
    return db.query(models.Product).filter(models.Product.id == id).first()


def put_product(
    db: Session,
    id: int,
    name: str = "",
    description: str = "",
    price: int = -1
):
    # パラメータ確認
    if name == description and price == -1:
        raise HTTPException(
            status_code=400,
            detail="Invalid request"
        )
    isExist = db.query(models.Product.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The product is not exist"
        )
    # アップデート
    product_update = db.query(models.Product).filter(
        models.Product.id == id
    ).first()
    if name:
        product_update.name = name
    if description:
        product_update.description = description
    if price != -1:
        product_update.price = price
    db.commit()
    return True


def delete_product(db: Session, id: int):
    isExist = db.query(models.Product.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The product is not exist"
        )
    db.query(models.UserInventory).filter(
        models.UserInventory.product_id == id
    ).delete()
    db.query(models.MachineInventory).filter(
        models.MachineInventory.product_id == id
    ).delete()
    db.query(models.Product).filter(
        models.Product.id == id
    ).delete()
    db.commit()
    return True


def list_machine(db: Session, page: int, sort: int, count: int):
    q = db.query(models.Machine)
    sortDict = {
        1: desc(models.Machine.id),
        2: asc(models.Machine.id),
        3: desc(models.Machine.name),
        4: asc(models.Machine.name)
    }
    if sort > 4:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset(page*count).all()
    return q


def create_machine(db: Session, name: str, products: List[int]):
    isExist = db.query(models.Machine.id).filter_by(
        name=name
    ).scalar() is not None
    if isExist:
        raise HTTPException(
            status_code=400,
            detail="The machine name is already used"
        )
    productList = db.query(models.Product).filter(
        models.Product.id.in_(products)
    ).all()
    newMachineRequest = models.Machine(
        name=name,
        products=productList
    )
    db.add(newMachineRequest)
    db.commit()
    return True


def get_machine(db: Session, id: int):
    isExist = db.query(models.Machine.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The machine is not exist"
        )
    return db.query(models.Machine).filter(models.Machine.id == id).first()


def put_machine(
    db: Session,
    id: int,
    name: str = "",
    products: List[int] = []
):
    # パラメータ確認
    if not name and not products:
        raise HTTPException(
            status_code=400,
            detail="Invalid request"
        )
    isExist = db.query(models.Machine.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The machine is not exist"
        )
    # アップデート
    machine_update = db.query(models.Machine).filter(
        models.Machine.id == id
    ).first()
    if name:
        machine_update.name = name
    if products:
        productList = db.query(models.Product).filter(
            models.Product.id.in_(products)
        ).all()
        machine_update.products = productList
    db.commit()
    return True


def delete_machine(db: Session, id: int):
    isExist = db.query(models.Machine.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The machine is not exist"
        )
    db.query(models.Machine).filter(
        models.Machine.id == id
    ).delete()
    db.commit()
    return True


def list_airdrop(db: Session, page: int, sort: int, count: int):
    q = db.query(models.Airdrop)
    sortDict = {
        1: desc(models.Airdrop.id),
        2: asc(models.Airdrop.id),
        3: desc(models.Airdrop.name),
        4: asc(models.Airdrop.name)
    }
    if sort > 4:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset(page*count).all()
    return q


def create_airdrop(
    db: Session,
    name: str,
    description: str,
    amount: int,
    interval: int
):
    isExist = db.query(models.Airdrop.id).filter_by(
        name=name
    ).scalar() is not None
    if isExist:
        raise HTTPException(
            status_code=400,
            detail="The airdrop name is already used"
        )
    newAirdropRequest = models.Airdrop(
        name=name,
        description=description,
        amount=amount,
        interval=interval
    )
    db.add(newAirdropRequest)
    db.commit()
    return True


def get_airdrop(db: Session, id: int):
    isExist = db.query(models.Airdrop.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The airdrop is not exist"
        )
    return db.query(models.Airdrop).filter(models.Airdrop.id == id).first()


def put_airdrop(
    db: Session,
    id: int,
    name: str = "",
    description: str = "",
    amount: int = 0,
    interval: int = 0
):
    # パラメータ確認
    if name == description and not amount and not interval:
        raise HTTPException(
            status_code=400,
            detail="Invalid request"
        )
    isExist = db.query(models.Airdrop.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The airdrop is not exist"
        )
    # アップデート
    airdrop_update = db.query(models.Airdrop).filter(
        models.Airdrop.id == id
    ).first()
    if name:
        airdrop_update.name = name
    if description:
        airdrop_update.description = description
    if amount:
        airdrop_update.amount = amount
    if interval:
        airdrop_update.interval = interval
    db.commit()
    return True


def delete_airdrop(db: Session, id: int):
    isExist = db.query(models.Airdrop.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The airdrop is not exist"
        )
    db.query(models.Airdrop).filter(
        models.Airdrop.id == id
    ).delete()
    db.commit()
    return True


def list_transactions(
    db: Session,
    user_id: int,
    page: int,
    sort: int,
    count: int
):
    q = db.query(models.Transaction).filter(
         or_(
             models.Transaction.provider == user_id,
         )
    )
    sortDict = {
        1: desc(models.Airdrop.id),
        2: asc(models.Airdrop.id),
        3: desc(models.Airdrop.name),
        4: asc(models.Airdrop.name)
    }
    if sort > 4:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset(page*count).all()
    return q