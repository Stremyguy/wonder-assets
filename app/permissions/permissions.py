from typing import Callable
from functools import wraps
from flask import flash, abort
from flask_login import current_user, UserMixin
from app.services import get_role_by_id
from app.models import Permission, RoleIDs

ANONYMOUS_PERMISSIONS = {
    Permission.VIEW_CATEGORY,
    Permission.VIEW_ITEM
}

ROLE_PERMISSIONS = {
    "user": {
        Permission.VIEW_CATEGORY,
        Permission.VIEW_ITEM,
        Permission.VIEW_OWN_CATEGORY,
        Permission.VIEW_OWN_ITEM,
        Permission.EDIT_OWN_PROFILE
    },
    "creator": {
        Permission.CREATE_CATEGORY, 
        Permission.EDIT_OWN_CATEGORY, 
        Permission.DELETE_OWN_CATEGORY,
        Permission.VIEW_OWN_CATEGORY,
        Permission.CREATE_ITEM,
        Permission.EDIT_OWN_ITEM,
        Permission.DELETE_OWN_ITEM,
        Permission.VIEW_OWN_ITEM,
        Permission.EDIT_OWN_PROFILE
    },
    "moderator": {
        Permission.CREATE_CATEGORY, 
        Permission.EDIT_CATEGORY, 
        Permission.DELETE_CATEGORY, 
        Permission.VIEW_CATEGORY, 
        Permission.VIEW_PRIVATE_CATEGORY,
        Permission.VIEW_PRIVATE_ITEM,
        Permission.CREATE_ITEM,
        Permission.EDIT_ITEM,
        Permission.DELETE_ITEM,
        Permission.EDIT_ADMIN_ITEM,
        Permission.DELETE_ADMIN_ITEM,
        Permission.EDIT_OWN_PROFILE
    },
    "admin": {
        Permission.CREATE_CATEGORY, 
        Permission.EDIT_CATEGORY, 
        Permission.DELETE_CATEGORY,
        Permission.VIEW_CATEGORY, 
        Permission.VIEW_PRIVATE_CATEGORY,
        Permission.CAN_VIEW_ADMIN_PANEL,
        Permission.VIEW_PRIVATE_ITEM,
        Permission.CREATE_ITEM,
        Permission.EDIT_ITEM,
        Permission.DELETE_ITEM,
        Permission.EDIT_ADMIN_ITEM,
        Permission.DELETE_ADMIN_ITEM,
        Permission.EDIT_ANY_PROFILE,
        Permission.DELETE_USER
    },
}


def get_role_name_by_id(role_id: int) -> str | None:
    """Helper function to get the role name based on the role_id."""
    role = get_role_by_id(role_id)
    return role.name if role else None


def has_permission(user: UserMixin, permission: str) -> bool:
    if not user.is_authenticated:
        return permission in ANONYMOUS_PERMISSIONS
    
    if RoleIDs.ADMIN in [role.id for role in user.roles]:
        return True
    
    role_ids = [role.id for role in user.roles]
    allowed_permissions = set()
    
    for role_id in role_ids:
        role_name = get_role_name_by_id(role_id)
        if role_name in ROLE_PERMISSIONS:
            allowed_permissions.update(ROLE_PERMISSIONS[role_name])
        
    return permission in allowed_permissions


def can_edit_profile(user: UserMixin, profile_owner_id: int) -> bool:
    """Check if a user can edit a specific profile."""
    if not user.is_authenticated:
        return False
    
    if has_permission(user, Permission.EDIT_ANY_PROFILE):
        return True
    
    return user.id == profile_owner_id and has_permission(user, Permission.EDIT_OWN_PROFILE)


def permission_required(permission: str) -> Callable:
    """Decorator to check if the current user has a specific permission."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: list, **kwargs: dict) -> object:
            if not current_user.is_authenticated:
                if permission not in ANONYMOUS_PERMISSIONS:
                    flash("You need to be logged in to access this page.", "error")
                    abort(403)
                return func(*args, **kwargs)
            
            if not has_permission(current_user, permission):
                flash("You don't have the necessary permission to access this page.", "error")
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
