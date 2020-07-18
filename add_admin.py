from itsdangerous import JSONWebSignatureSerializer as Serializer
from routers import database, crud


if __name__ == "__main__":
    db = database.SessionLocal()
    userName = input("Input new admin name >>:")
    userPass = input("Input new admin password >>:")
    admin_token = crud.create_admin(db, userName, userPass)
    print(f"Admin token is {admin_token}")
    db.close()
