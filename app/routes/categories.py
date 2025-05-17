from flask import Blueprint, render_template, redirect, request, abort
from flask_login import login_required, current_user
from app.services import (get_category_by_id, 
                          get_all_categories, 
                          get_all_roles, 
                          filter_visible_categories,
                          get_items_by_category_id,
                          filter_visible_items)
from app.services import create_category as create_category_service
from app.services import edit_category as edit_category_service
from app.services import delete_category as delete_category_service
from app.permissions import has_permission, permission_required
from app.models import RoleIDs, Permission
from app.forms import CategoryForm

category_bp = Blueprint("categories", __name__)


@category_bp.route("/")
def categories_page() -> str:
    all_categories = get_all_categories()
    visible_categories = filter_visible_categories(all_categories, current_user)
    visible_categories = sorted(visible_categories, key=lambda c: c.title)
    
    can_create = has_permission(current_user, Permission.CREATE_CATEGORY) if current_user.is_authenticated else False
    private_access = has_permission(current_user, Permission.VIEW_PRIVATE_CATEGORY) if current_user.is_authenticated else False
    
    params = {
        "title": "Wonder assets",
        "categories": visible_categories,
        "can_create": can_create,
        "private_access": private_access,
    }
    
    return render_template("index.html", **params)


@category_bp.route("/categories/<int:category_id>")
def category_page(category_id: int) -> str:
    category = get_category_by_id(category_id)
    
    if not category:
        abort(404)
    
    search_query = request.args.get("q")
    sort_option = request.args.get("sort", "date_desc")
    
    items = get_items_by_category_id(
        category_id,
        search_query=search_query,
        sort_by=sort_option
    )
    
    visible_items = filter_visible_items(items, current_user)
    
    @login_required
    def get_info_about_creator() -> bool:
        is_creator = category.creator_id == current_user.id
        can_edit_own = has_permission(current_user, Permission.EDIT_OWN_CATEGORY)
        can_edit_all = has_permission(current_user, Permission.EDIT_CATEGORY)
        can_delete_own = has_permission(current_user, Permission.DELETE_OWN_CATEGORY)
        can_delete_all = has_permission(current_user, Permission.DELETE_CATEGORY)
        
        return (is_creator and (can_edit_own and can_delete_own)) or (can_edit_all and can_delete_all)

    can_change_data = get_info_about_creator() if current_user.is_authenticated else False
    
    params = {
        "title": "Wonder assets",
        "category": category,
        "items": visible_items if visible_items else None,
        "can_change_data": can_change_data,
    }
    
    return render_template("category.html", **params)


@category_bp.route("/categories/create", methods=["GET", "POST"])
@login_required
@permission_required(Permission.CREATE_CATEGORY)
def create_category() -> str:
    form = CategoryForm()
    roles = get_all_roles()
    form.visible_to_roles.choices = [(role.id, role.name) for role in roles]
    
    current_role_ids = [role.id for role in current_user.roles]
    disabled_roles = []
    default_roles = [RoleIDs.USER]
    
    if RoleIDs.ADMIN in current_role_ids or RoleIDs.MODERATOR in current_role_ids:
        default_roles.append(RoleIDs.ADMIN)
        disabled_roles.append(RoleIDs.ADMIN)
    
    elif RoleIDs.CREATOR in current_role_ids:
        default_roles.extend([RoleIDs.MODERATOR, RoleIDs.ADMIN])
        disabled_roles.extend([RoleIDs.MODERATOR, RoleIDs.ADMIN])

    if request.method == "GET" or not form.validate_on_submit():
        form.visible_to_roles.data = list(set(default_roles))
    
    params = {
        "title": "Wonder assets",
        "form": form,
        "disabled_roles": disabled_roles,
    }
    
    if form.validate_on_submit():
        create_category_service(
            title=form.title.data,
            short_description=form.short_description.data,
            full_description=form.full_description.data,
            creator_id=current_user.id,
            role_ids=form.visible_to_roles.data,
            is_private=form.is_private.data,
            is_testing=form.is_testing.data
        )
        
        return redirect("/")
    return render_template("category_form.html", **params)


@category_bp.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id: int) -> str:
    category = get_category_by_id(category_id)
    
    if not category:
        abort(404)
    
    is_creator = category.creator_id == current_user.id
    can_edit_own = has_permission(current_user, Permission.EDIT_OWN_CATEGORY)
    can_edit_all = has_permission(current_user, Permission.EDIT_CATEGORY)
    
    if not ((is_creator and can_edit_own) or can_edit_all):
        abort(403)
    
    form = CategoryForm()
    roles = get_all_roles()
    form.visible_to_roles.choices = [(role.id, role.name) for role in roles]
    
    current_role_ids = [role.id for role in current_user.roles]
    disabled_roles = []
    locked_roles = []
    
    if RoleIDs.ADMIN in current_role_ids or RoleIDs.MODERATOR in current_role_ids:
        locked_roles.append(RoleIDs.ADMIN)
        disabled_roles.append(RoleIDs.ADMIN)
    
    elif RoleIDs.CREATOR in current_role_ids:
        locked_roles.extend([RoleIDs.MODERATOR, RoleIDs.ADMIN])
        disabled_roles.extend([RoleIDs.MODERATOR, RoleIDs.ADMIN])
    
    if request.method == "GET":
        form.title.data = category.title
        form.short_description.data = category.short_description
        form.full_description.data = category.full_description
        form.visible_to_roles.data = [role.id for role in category.visible_to_roles]
        form.is_private.data = category.is_private
        form.is_testing.data = category.is_testing

        existing_roles = [role.id for role in category.visible_to_roles]
        final_roles = list(set(existing_roles + locked_roles))
        form.visible_to_roles.data = final_roles
    
    elif form.validate_on_submit():
        submitted_roles = form.visible_to_roles.data
        
        submitted_roles = list(set(submitted_roles + locked_roles))
        
        edit_category_service(
            category_id=category_id,
            title=form.title.data,
            short_description=form.short_description.data,
            full_description=form.full_description.data,
            role_ids=submitted_roles,
            is_private=form.is_private.data,
            is_testing=form.is_testing.data
        )
        return redirect("/")

    params = {
        "title": "Wonder assets",
        "form": form,
        "disabled_roles": disabled_roles,
    }
    
    return render_template("category_form.html", **params)


@category_bp.route("/categories/delete/<int:category_id>", methods=["GET", "POST"])
@login_required
def delete_category(category_id: int) -> str:
    category = get_category_by_id(category_id)
    if not category:
        abort(404)
    
    is_creator = category.creator_id == current_user.id
    can_delete_own = has_permission(current_user, Permission.DELETE_OWN_CATEGORY)
    can_delete_all = has_permission(current_user, Permission.DELETE_CATEGORY)
    
    if not (is_creator and can_delete_own) and not can_delete_all:
        abort(403)
    
    delete_category_service(category_id)    
    return redirect("/")
