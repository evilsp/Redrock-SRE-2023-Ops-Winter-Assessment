from mysql import Session, User


def checkpwd(pwd: str):
    if len(pwd) < 6:
        return False
    else:
        return True


def checkusername(username: str):
    users = Session.query(User).all()
    Session.close()
    for user in users:
        if user.username == username:
            return False
    return True
