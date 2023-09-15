from app.config import session
from app.model import Collaborator, StatusEnum, RoleEnum
from sqlalchemy import literal_column


def display_contract_status(value):
    if value == 1:
        return "created"
    elif value == 2:
        return "signed"
    elif value == 3:
        return "paid"
    else:
        return "Invalid status"


def display_role_status(value):
    if value == 1:
        return "sales"
    elif value == 2:
        return "support"
    elif value == 3:
        return "manager"
    else:
        return "Invalid role"


def get_current_user():
    current_user = session.query(literal_column("current_user"))
    for usr in current_user:
        return usr[0]


def get_role(current_user):
    collaborators = session.query(Collaborator).all()
    for collaborator in collaborators:
        if collaborator.name == current_user:
            return collaborator.role
