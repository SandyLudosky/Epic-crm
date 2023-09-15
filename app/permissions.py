from .models import RoleEnum as UserRole
from utils import get_current_user


class UserPermissions:

    # CRUD permissions on table collarborator
    @staticmethod
    def can_create_collaborator(current_user: UserRole) -> bool:
        return True if current_user.role == UserRole.manager else False

    @staticmethod
    def can_update_collaborator(current_user: UserRole) -> bool:
        return True if current_user.role == UserRole.manager else False

    @staticmethod
    def can_delete_collaborator(current_user: UserRole) -> bool:
        return True if current_user == UserRole.manager else False

    # CRUD permissions on table contract
    def can_create_contract(current_user: UserRole) -> bool:
        return True if current_user == UserRole.manager else False

    @staticmethod
    def can_update_contract(current_user: UserRole) -> bool:
        return True if current_user == UserRole.manager else False

    # CRUD permissions on table client
    @staticmethod
    def can_create_client(current_user: UserRole) -> bool:
        return True if current_user == UserRole.admin else False

    @staticmethod
    def can_update_user(current_user: UserRole) -> bool:
        return True if current_user == UserRole.admin else False

    @staticmethod
    def can_delete_user(current_user: UserRole) -> bool:
        return True if current_user == UserRole.admin else False

    # CRUD permissions on table event

    @staticmethod
    def can_display_events_without_support(current_user: UserRole) -> bool:
        return True if current_user == UserRole.manager else False

    def can_update_events_without_support(current_user: UserRole) -> bool:
        return True if current_user == UserRole.manager else False

    @staticmethod
    def can_update_event(user_id: int, user_role: UserRole) -> bool:
        pass

    @staticmethod
    def can_delete_event(user_id: int, user_role: UserRole) -> bool:
        pass
