from flask import Blueprint, render_template
from app.services import get_all_roles, get_all_users
from app.permissions import permission_required

admin_bp = Blueprint("admin_panel", __name__, url_prefix="/admin_panel")


@admin_bp.route("/", methods=["GET", "POST"])
@permission_required("can_view_admin_panel")
def dashboard() -> str:
    roles = get_all_roles()
    users = get_all_users()
    
    params = {
        "title": "Dashboard",
        "roles": roles,
        "users": users,
    }
    
    return render_template("dashboard.html", **params)
