from app.config import session
from app.models import User, ROLE, STATUS
from sqlalchemy import literal_column


def display_contract_status(value):
    if int(value) == 1:
        return STATUS["CREATED"]
    elif int(value) == 2:
        return STATUS["SIGNED"]
    elif int(value) == 3:
        return STATUS["PAID"]
    else:
        return "Invalid status"


def get_role(role):
    if int(role) == 1:
        return ROLE["SALES"]
    elif int(role) == 2:
        return ROLE["SUPPORT"]
    elif int(role) == 3:
        return ROLE["MANAGER"]
    else:
        print("Invalid role")


def get_current_username():
    current_user = session.query(literal_column("current_user"))
    for usr in current_user:
        return usr[0]


def get_current_user():
    current_user = get_current_username()
    user = session.query(User).all()
    for user in user:
        if user.name == current_user:
            return user

# MENU


def restart():
    print("======== MENU =========")
    print("[1] - make another query")
    print("[2] - quit")
    print("=========================")
