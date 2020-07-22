from sqlalchemy.orm import Session
from sqlalchemy.sql import text, desc, asc, or_, and_
from fastapi import HTTPException
from typing import List
from . import models, schemas
from .database import SALT
from .authorizator import generate_token
from hashlib import sha256
import datetime
import random


def list_user(db: Session, page: int, sort: int, count: int):
    q = db.query(models.User)
    user_count = db.query(models.User).count()
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
    q = q.limit(count).offset((page-1)*count).all()
    return q, user_count


def create_admin(db: Session, name: str, password: str):
    # 重複するアカウント禁止
    isExist = db.query(models.User.id).filter_by(
        name=name
    ).scalar() is not None
    if isExist:
        raise Exception("The name is already in use.")
    # 新規ユーザー作成
    newUserRequest = models.User(
        name=name,
        password=sha256(
            (SALT + password).encode("utf-8")
        ).hexdigest(),
        is_admin=1
    )
    db.add(newUserRequest)
    db.commit()
    # トークン作成
    newUser = db.query(models.User.id).filter_by(
        name=name
    ).first()
    token = generate_token(db, newUser.id, 1)
    return token


def create_user(db: Session, new_user: schemas.UserCreateRequest):
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
    token = generate_token(db, newUser.id, 0)
    return token


def get_user(db: Session, user_id: int, with_inventory: bool):
    isExist = db.query(models.User.id).filter_by(
        id=user_id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The user is not exist"
        )
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if with_inventory:
        user_inventory = db.query(
            models.Product
        ).join(
            models.UserInventory
        ).filter(
            models.UserInventory.user_id == user_id
        ).all()
        return user, user_inventory
    return user


def put_user(
    db: Session,
    user_id: int,
    name: str = '',
    money: int = None,
    is_admin: bool = None
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
    # TODO: Replace transactions with deleted-user account
    db.query(models.Transaction).filter(
        or_(
            models.Transaction.provider == id,
            models.Transaction.receiver == id
        )
    ).delete()
    db.commit()
    return True


def list_product(db: Session, page: int, sort: int, count: int):
    q = db.query(models.Product)
    product_count = db.query(models.Product).count()
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
    q = q.limit(count).offset((page-1)*count).all()
    return q, product_count


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


def buy_product(db: Session, user_id: int, product_id: int):
    isExist = db.query(models.User.id).filter_by(
        id=user_id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The user is not exist"
        )
    isExist = db.query(models.Product.id).filter_by(
        id=product_id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The product is not exist"
        )
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()
    if user.money < product.price:
        raise HTTPException(
            status_code=402,
            detail="Not enough money"
        )
    user.money -= product.price
    addInventoryRequest = models.UserInventory(
        user_id=user_id,
        product_id=product_id
    )
    db.add(addInventoryRequest)
    newTransactionRequest = models.Transaction(
        provider_type=0,
        provider=user_id,
        receiver_type=2,
        receiver=product_id,
        amount=product.price
    )
    db.add(newTransactionRequest)
    db.commit()
    return True


def list_machine(db: Session, page: int, sort: int, count: int):
    q = db.query(models.Machine)
    machine_count = db.query(models.Product).count()
    sortDict = {
        1: desc(models.Machine.id),
        2: asc(models.Machine.id),
        3: desc(models.Machine.name),
        4: asc(models.Machine.name)
    }
    if sort > 4:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset((page-1)*count).all()
    return q, machine_count


def create_machine(
    db: Session,
    name: str,
    description: str,
    products: List[int]
):
    isExist = db.query(models.Machine.id).filter_by(
        name=name
    ).scalar() is not None
    if isExist:
        raise HTTPException(
            status_code=400,
            detail="The machine name is already used"
        )
    productList = [
        models.MachineInventory(
            product_id=p
        )
        for p in products
    ]
    print(productList)
    newMachineRequest = models.Machine(
        name=name,
        description=description,
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
    machine = db.query(models.Machine).filter(models.Machine.id == id).first()
    machine_inventory = db.query(
        models.Product
    ).join(
        models.MachineInventory
    ).filter(
        models.MachineInventory.machine_id == id
    ).all()
    return machine, machine_inventory


def put_machine(
    db: Session,
    id: int,
    name: str = "",
    description: str = "",
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
    if str(name) != "<class 'pydantic.types.ConstrainedStrValue'>" and name != "":
        machine_update.name = name
    if str(description) != "<class 'pydantic.types.ConstrainedStrValue'>" and name != "":
        machine_update.description = description
    if products:
        products = list(set(products))
        db.query(models.MachineInventory).filter(
            models.MachineInventory.machine_id == id
        ).delete()
        newMachineInventory = [
            models.MachineInventory(
                machine_id=id,
                product_id=p
            )
            for p in products
        ]
        machine_update.products = newMachineInventory
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
    airdrop_count = db.query(models.Airdrop).count()
    sortDict = {
        1: desc(models.Airdrop.id),
        2: asc(models.Airdrop.id),
        3: desc(models.Airdrop.name),
        4: asc(models.Airdrop.name)
    }
    if sort > 4:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset((page-1)*count).all()
    return q, airdrop_count


def list_airdrop_with_stat(db: Session, page: int, sort: int, count: int, user_id: int):
    q = db.query(models.Airdrop)
    airdrop_count = db.query(models.Airdrop).count()
    sortDict = {
        1: desc(models.Airdrop.id),
        2: asc(models.Airdrop.id),
        3: desc(models.Airdrop.name),
        4: asc(models.Airdrop.name)
    }
    if sort > 4:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset((page - 1) * count).all()
    resp = []
    # Javascriptを想定して "2008-05-01T02:00:00+09:00" という型にする
    requested_date = datetime.datetime.now()
    for airdrop in q:
        data = {
            "id": airdrop.id,
            "name": airdrop.name,
            "description": airdrop.description,
            "amount": airdrop.amount,
            "interval": airdrop.interval,
            "receivable": True,
            "next_receivable": requested_date.strftime(
                '%Y-%m-%dT%H:%M:%S+09:00'
            )
        }
        last_transaction = db.query(models.Transaction).order_by(
            desc(models.Transaction.id)
        ).filter(
            models.Transaction.provider_type == 1,
            models.Transaction.provider == airdrop.id,
            models.Transaction.receiver_type == 0,
            models.Transaction.receiver == user_id
        ).first()
        if last_transaction:
            # 次に受け取れる日時
            receivable_date = last_transaction.reception
            # 要求日時
            # 経過した分数を見る
            if airdrop.mode == 0:
                receivable_date += datetime.timedelta(minutes=airdrop.interval)
            # 経過した日数を見る
            else:
                receivable_date += datetime.timedelta(days=airdrop.interval)
                receivable_date = receivable_date.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0
                )
            # 要求した時刻が 受け取りできる時刻以下ならエラー
            if receivable_date > requested_date:
                data["receivable"] = False
                data["next_receivable"] = receivable_date.strftime(
                    '%Y-%m-%dT%H:%M:%S+09:00'
                )
        resp.append(data)
    return resp, airdrop_count


def create_airdrop(
    db: Session,
    name: str,
    description: str,
    amount: int,
    interval: int,
    mode: int
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
        interval=interval,
        mode=mode
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


def get_airdrop_with_stat(db: Session, id: int, user_id: int):
    isExist = db.query(models.Airdrop.id).filter_by(
        id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The airdrop is not exist"
        )
    requested_date = datetime.datetime.now()
    airdrop = db.query(models.Airdrop).filter(models.Airdrop.id == id).first()
    data = {
        "text": "ok",
        "id": airdrop.id,
        "name": airdrop.name,
        "description": airdrop.description,
        "amount": airdrop.amount,
        "interval": airdrop.interval,
        "receivable": True,
        "next_receivable": requested_date.strftime(
            '%Y-%m-%dT%H:%M:%S+09:00'
        )
    }
    last_transaction = db.query(models.Transaction).order_by(
        desc(models.Transaction.id)
    ).filter(
        models.Transaction.provider_type == 1,
        models.Transaction.provider == airdrop.id,
        models.Transaction.receiver_type == 0,
        models.Transaction.receiver == user_id
    ).first()
    if last_transaction:
        # 次に受け取れる日時
        receivable_date = last_transaction.reception
        # 要求日時
        # 経過した分数を見る
        if airdrop.mode == 0:
            receivable_date += datetime.timedelta(minutes=airdrop.interval)
        # 経過した日数を見る
        else:
            receivable_date += datetime.timedelta(days=airdrop.interval)
            receivable_date = receivable_date.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
        # 要求した時刻が 受け取りできる時刻以下ならエラー
        if receivable_date > requested_date:
            data["receivable"] = False
            data["next_receivable"] = receivable_date.strftime(
                '%Y-%m-%dT%H:%M:%S+09:00'
            )
    return data

def put_airdrop(
    db: Session,
    id: int,
    name: str = "",
    description: str = "",
    amount: int = -1,
    interval: int = -1,
    mode: int = -1
):
    # パラメータ確認
    if name == description and amount == -1 and interval == -1 and mode == -1:
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
    if amount != -1:
        airdrop_update.amount = amount
    if interval != -1:
        airdrop_update.interval = interval
    if mode != -1:
        airdrop_update.mode = mode
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


def claim_airdrop(db: Session, airdrop_id: int, user_id: int):
    isExist = db.query(models.User.id).filter_by(
        id=user_id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The user is not exist"
        )
    isExist = db.query(models.Airdrop.id).filter_by(
        id=airdrop_id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The airdrop is not exist"
        )
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    airdrop = db.query(
        models.Airdrop
    ).filter(
        models.Airdrop.id == airdrop_id
    ).first()
    last_transaction = db.query(models.Transaction).order_by(
        desc(models.Transaction.id)
    ).filter(
        models.Transaction.provider_type == 1,
        models.Transaction.provider == airdrop_id,
        models.Transaction.receiver_type == 0,
        models.Transaction.receiver == user_id
    ).first()
    before_money = user.money
    if last_transaction:
        # 次に受け取れる日時
        receivable_date = last_transaction.reception
        # 要求日時
        requested_date = datetime.datetime.now()
        # 0: 経過した分数を見る
        if airdrop.mode == 0:
            receivable_date += datetime.timedelta(minutes=airdrop.interval)
        # 1/2/3 : 経過した日数を見る
        elif airdrop.mode < 4:
            receivable_date += datetime.timedelta(days=airdrop.interval)
            receivable_date = receivable_date.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
        # 要求した時刻が 受け取りできる時刻以下ならエラー
        if receivable_date > requested_date:
            raise HTTPException(
                status_code=429,
                detail="The airdrop can not recieve for now."
            )
    # 0/1: Normal
    if airdrop.mode < 2:
        transaction_amount = airdrop.amount
    # 2: Gacha1
    elif airdrop.mode == 2:
        prizes = [1, 2, 5, 10]
        weight = [73, 20, 5, 2]
        transaction_amount = random.choices(prizes, weight, k=1)[0]
    # 3: Gacha2
    else:
        prizes = [5, 10, 20, 30]
        weight = [85, 10, 4, 1]
        transaction_amount = random.choices(prizes, weight, k=1)[0]
    user.money += transaction_amount
    after_money = user.money
    newTransactionRequest = models.Transaction(
        provider_type=1,
        provider=airdrop_id,
        receiver_type=0,
        receiver=user_id,
        amount=transaction_amount
    )
    db.add(newTransactionRequest)
    db.commit()
    return True, before_money, after_money


def list_transaction(
    db: Session,
    user_id: int,
    page: int,
    sort: int,
    count: int
):
    q = db.query(models.Transaction).filter(
         or_(
             and_(
                models.Transaction.provider == user_id,
                models.Transaction.provider_type == 0
             ),
             and_(
                models.Transaction.receiver == user_id,
                models.Transaction.receiver_type == 0
             )
         )
    )
    transaction_count = q.count()
    sortDict = {
        1: desc(models.Transaction.id),
        2: asc(models.Transaction.id)
    }
    if sort > 2:
        sort = 1
    q = q.order_by(sortDict[sort])
    q = q.limit(count).offset((page-1)*count).all()
    return q, transaction_count


def create_transaction(
    db: Session,
    provider_type: int,
    provider_id: int,
    receiver_type: int,
    receiver_id: int
):
    newTransactionRequest = models.Transaction(
        provider_type=provider_type,
        provider_id=provider_id,
        receiver_type=receiver_type,
        receiver_id=receiver_id
    )
    db.add(newTransactionRequest)
    db.commit()
    return True


def delete_transaction(db: Session, id: int):
    isExist = db.query(models.Transaction.transaction_id).filter_by(
        transaction_id=id
    ).scalar() is not None
    if not isExist:
        raise HTTPException(
            status_code=404,
            detail="The transaction is not exist"
        )
    db.query(models.Transaction).filter(
        models.Transaction.id == id
    ).delete()
    db.commit()
    return True
