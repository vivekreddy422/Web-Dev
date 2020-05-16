from models import *
from sqlalchemy import and_

def get_user_details(userName = None, password = None):
    if userName is None or password is None:
        return False
    else:
        users = User.query.filter(and_(User.userName == userName,User.password == password)).first()
        if (users is None):
            return False
        return True


def register_user(userName = None, password = None):
    try:
        db.session.commit()
        if userName is None or password is None:
            return False
        newUser = User(userName = userName, password = password)
        db.session.add(newUser)
        db.session.commit()
        return True
    except Exception as e:
        return False