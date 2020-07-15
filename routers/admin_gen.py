from itsdangerous import JSONWebSignatureSerializer as Serializer


def create_admin_token(authSalt, authSeq, userID):
    token_serializer = Serializer(authSalt)
    token = token_serializer.dumps({
        'id': userID,
        'seq': authSeq + 1,
        'is_admin': 1
    }).decode('utf-8')
    return token, authSeq + 1


if __name__ == "__main__":
    authSalt = str(input("Input SALT >>:"))
    userID = int(input("Input User ID >>:"))
    authSeq = int(input("Input Auth seq >>:"))
    admin_token, admin_seq = create_admin_token(authSalt, authSeq, userID)
    print(f"Admin token is {admin_token}, and Admin Seq is {admin_seq}")