from flask import Blueprint, render_template
from app.services import get_user_by_id

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile/<int:user_id>")
def profile_page(user_id: int) -> str:
    user = get_user_by_id(user_id)
    params = {
        "title": "Wonder assets",
        "user_id": user_id,
        "user": user,
    }
    
    return render_template("profile.html", **params)
