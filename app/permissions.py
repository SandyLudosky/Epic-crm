from .models import Client, RoleEnum as UserRole
from app.config import session


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
    @staticmethod
    def can_create_contract(current_user: UserRole) -> bool:
        return True if current_user == UserRole.manager else False

    @staticmethod
    def can_read_contract(current_user: UserRole) -> bool:
        return True if current_user == UserRole.sales else False

    @staticmethod
    def can_update_contract(current_user: UserRole) -> bool:
        return True if current_user in [UserRole.manager, UserRole.sales] else False

    # CRUD permissions on table client
    @staticmethod
    def can_create_client(current_user: UserRole) -> bool:
        return True if current_user == UserRole.sales else False

    @staticmethod
    def can_update_client(current_user: UserRole) -> bool:
        return True if current_user == UserRole.sales else False

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
