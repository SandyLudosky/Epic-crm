from app.model import StatusEnum, RoleEnum


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
