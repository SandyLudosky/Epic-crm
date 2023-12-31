from .models import ROLE
from app.config import session
from app.auth import (
    get_current_user,
)


class UserPermissions:

    # CRUD permissions on table collarborator
    @staticmethod
    def can_create_user() -> bool:
        current_user = get_current_user()
        return True if current_user.role == ROLE["MANAGER"] else False

    @staticmethod
    def can_update_user() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["MANAGER"] else False

    @staticmethod
    def can_delete_user() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["MANAGER"] else False

    # CRUD permissions on table contract
    @staticmethod
    def can_create_contract() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["MANAGER"] else False

    @staticmethod
    def can_read_contract() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role in [ROLE["SALES"], ROLE["MANAGER"]] else False

    @staticmethod
    def can_update_contract() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role in [ROLE["SALES"], ROLE["MANAGER"]] else False

    # CRUD permissions on table client
    @staticmethod
    def can_create_client() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["SALES"] else False

    @staticmethod
    def can_update_client() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["SALES"] else False

    # CRUD permissions on table event

    @staticmethod
    def can_display_events_without_support() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["MANAGER"] else False

    @staticmethod
    def can_update_events_without_support() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["MANAGER"] else False

    @staticmethod
    def can_support_read_events() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["SUPPORT"] else False

    @staticmethod
    def can_manager_read_events() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["MANAGER"] else False

    @staticmethod
    def can_create_event() -> bool:
        pass

    @staticmethod
    def can_update_event() -> bool:
        current_user = get_current_user(session)
        return True if current_user.role == ROLE["SALES"] else False
