from enum import Enum


class RoleIDs(int, Enum):
    """Role IDs used across the application (match database values)"""
    USER = 1
    CREATOR = 2
    MODERATOR = 3
    ADMIN = 4


class Permission(str, Enum):
    """Permission types (sync with ROLE_PERMISSION in permissions.py)"""
    EDIT_OWN_PROFILE = "edit_own_profile"
    EDIT_ANY_PROFILE = "edit_any_profile"
    DELETE_USER = "delete_user"
    
    # Categories
    VIEW_CATEGORY = "view_category"
    VIEW_PRIVATE_CATEGORY = "view_private_category"
    CREATE_CATEGORY = "create_category"
    EDIT_OWN_CATEGORY = "edit_own_category"
    EDIT_CATEGORY = "edit_category"
    DELETE_OWN_CATEGORY = "delete_own_category"
    DELETE_CATEGORY = "delete_category"
    VIEW_OWN_CATEGORY = "view_own_category"

    # Items
    VIEW_ITEM = "view_item"
    VIEW_PRIVATE_ITEM = "view_private_item"
    VIEW_OWN_ITEM = "view_own_item"
    CREATE_ITEM = "create_item"
    EDIT_ITEM = "edit_item"
    EDIT_OWN_ITEM = "edit_own_item"
    DELETE_ITEM = "delete_item"
    DELETE_OWN_ITEM = "delete_own_item"
    EDIT_ADMIN_ITEM = "edit_admin_item"
    DELETE_ADMIN_ITEM = "delete_admin_item"
    
    # Admin
    CAN_VIEW_ADMIN_PANEL = "can_view_admin_panel"
