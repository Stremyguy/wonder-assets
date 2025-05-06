from typing import Callable
from functools import wraps
from flask import flash, abort
from flask_login import current_user, UserMixin
from app.services import get_role_by_id

ROLE_PERMISSIONS = {
    "user": {
        "view_category"},
    "creator": {
        "create_category", 
        "edit_own_category", 
        "delete_own_category",
        "view_own_category",
        "create_item",
        "edit_own_item",
        "delete_own_item"},
    "moderator": {
        "create_category", 
        "edit_category", 
        "delete_category", 
        "view_category", 
        "view_private_category",
        "can_view_admin_panel",
        "view_private_item",
        "create_item",
        "edit_item",
        "delete_item"},
    "admin": {"create_category", 
              "edit_category", 
              "delete_category",
              "view_category", 
              "view_private_category",
              "can_view_admin_panel",
              "view_private_item",
              "create_item",
              "edit_item",
              "delete_item"},
}


def get_role_name_by_id(role_id: int) -> str | None:
    """Helper function to get the role name based on the role_id."""
    role = get_role_by_id(role_id)
    return role.name if role else None


def has_permission(user: UserMixin, permission: str) -> bool:
    role_ids = [role.id for role in user.roles]
    allowed_permissions = []
    
    for role_id in role_ids:
        role_name = get_role_name_by_id(role_id)
        allowed_permissions.extend(ROLE_PERMISSIONS.get(role_name, []))
        
    return permission in allowed_permissions


def permission_required(permission: str) -> Callable:
    """Decorator to check if the current user has a specific permission."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: list, **kwargs: dict) -> object:
            if not has_permission(current_user, permission):
                flash("You don't have the necessary permission to access this page.", "error")
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator
