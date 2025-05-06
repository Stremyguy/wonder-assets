from enum import Enum


class RoleIDs(int, Enum):
    """Role IDs used across the application (match database values)"""
    USER = 1
    CREATOR = 2
    MODERATOR = 3
    ADMIN = 4


class Permission(str, Enum):
    """Permission types (sync with ROLE_PERMISSION in permissions.py)"""
    VIEW_CATEGORY = "view_category"
    ...