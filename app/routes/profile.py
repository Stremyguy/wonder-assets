from flask import Blueprint, render_template, abort, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from app.services import get_user_by_id, get_items_by_creator_id, edit_user, change_user_roles
from app.permissions import has_permission, can_edit_profile
from app.models import Permission
from app.forms import ProfileForm
from flask_wtf import FlaskForm

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile/<int:user_id>")
def profile_page(user_id: int) -> str:
    user = get_user_by_id(user_id)
    all_items = get_items_by_creator_id(user_id)

    visible_items = []
    for item in all_items:
        if not item.is_private:
            visible_items.append(item)
        elif current_user.is_authenticated and (
            item.creator_id == current_user.id or
            has_permission(current_user, Permission.VIEW_PRIVATE_ITEM)
        ):
            visible_items.append(item)
    
    
    can_edit = current_user.is_authenticated and (
        current_user.id == user.id or 
        has_permission(current_user, Permission.EDIT_ANY_PROFILE)
    )
    
    params = {
        "title": "Wonder assets",
        "user_id": user_id,
        "user": user,
        "items": visible_items,
        "can_edit": can_edit
    }

    return render_template("profile.html", **params)


@profile_bp.route("/profile/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_profile(user_id: int) -> str:
    user = get_user_by_id(user_id)
    if not user:
        abort(404)
    
    if not can_edit_profile(current_user, user.id):
        flash("You don't have permission to edit this profile", "error")
        abort(403)
    
    form = ProfileForm()
    
    
    show_role_management = (
        has_permission(current_user, Permission.EDIT_ANY_PROFILE) and
        current_user.id != user.id
    )
    
    if request.method == "GET":
        form.username.data = user.username
        form.email.data = user.email
        form.bio.data = user.bio
        form.roles.data = [role.id for role in user.roles]
    
    if form.validate_on_submit():
        try:
            avatar_url = None
            if form.avatar.data:
                from app.services import update_user_avatar
                
                updated_user = update_user_avatar(form.avatar.data, user_id)
                if updated_user:
                    avatar_url = updated_user.avatar_url
                else:
                    flash("Failed to update profile picture. Please try again.", "error")
                    return redirect(url_for("profile.edit_profile", user_id=user_id))
                
            edit_user(
                user_id=user_id,
                username=form.username.data,
                bio=form.bio.data,
                avatar_url=avatar_url
            )
            
            if has_permission(current_user, Permission.EDIT_ANY_PROFILE) and current_user.id != user.id:
                change_user_roles(user_id, form.roles.data)
    
            flash("Profile updated successfully!", "success")
            return redirect(url_for("profile.profile_page", user_id=user_id))
            
        except Exception as exc:
            current_app.logger.error(f"Error editing profile: {str(exc)}")
            flash("Error editing profile. Please try again.", "error")
        
    return render_template("profile_form.html",
                           title="Wonder assets",
                           form=form,
                           user=user,
                           show_role_management=show_role_management)


@profile_bp.route("/profile/delete/<int:user_id>", methods=["GET", "POST"])
@login_required
def delete_user(user_id: int):
    user_to_delete = get_user_by_id(user_id)
    
    if not user_to_delete:
        abort(404)
    
    if not (current_user.id == user_id or
            has_permission(current_user, Permission.DELETE_USER)):
        flash("You don't have permission to delete this user", "error")
        abort(403)
    
    try:
        from app.services import delete_user as delete_user_service
        from flask_login import logout_user
        
        delete_user_service(user_id)
        flash("User deleted successfully", "success")
        
        if current_user.id == user_id:
            logout_user()
            return redirect(url_for("/"))
        
        return redirect(url_for("admin_panel.dashboard"))
    except Exception as e:
        current_app.logger.error(f"Error deleting user: {str(e)}")
        flash("Error deleting user", "error")
        return redirect(url_for("profile.profile_page", user_id=user_id))