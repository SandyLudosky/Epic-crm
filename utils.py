from app.model import StatusEnum, RoleEnum


def display_contract_status(value):
    if value == StatusEnum.created:
        return "created"
    elif value == StatusEnum.signed:
        return "signed"
    elif value == StatusEnum.paid:
        return "paid"
    else:
        return "Invalid status"


def display_role_status(value):
    if value == RoleEnum.sales:
        return "sales"
    elif value == RoleEnum.support:
        return "support"
    elif value == RoleEnum.manager:
        return "manager"
    else:
        return "Invalid role"
