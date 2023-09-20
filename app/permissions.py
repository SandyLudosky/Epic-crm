import os
from .models import Collaborator, RoleEnum as UserRole
from app.config import session


USER = os.getenv('USER')

def get_current_user():
    return session.query(Collaborator).filter(Collaborator.name == USER).first()

class UserPermissions:

    # CRUD permissions on table collarborator
    @staticmethod
    def can_create_collaborator() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.manager else False


    @staticmethod
    def can_update_collaborator() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.manager else False

    @staticmethod
    def can_delete_collaborator() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.manager else False

    # CRUD permissions on table contract
    @staticmethod
    def can_create_contract() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.manager else False


    @staticmethod
    def can_read_contract() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.sales else False


    @staticmethod
    def can_update_contract() -> bool:
        current_user = get_current_user()
        return True if current_user in [UserRole.manager, UserRole.sales] else False

    # CRUD permissions on table client
    @staticmethod
    def can_create_client() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.sales else False

    @staticmethod
    def can_update_client() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.sales else False

    # CRUD permissions on table event

    @staticmethod
    def can_display_events_without_support() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.manager else False

    def can_update_events_without_support() -> bool:
        current_user = get_current_user()
        return True if current_user.role == UserRole.manager else False

    @staticmethod
    def can_update_event(user_id: int, user_role: UserRole) -> bool:
        pass

    @staticmethod
    def can_delete_event(user_id: int, user_role: UserRole) -> bool:
        pass
