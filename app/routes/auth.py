from flask import Blueprint, render_template, url_for, redirect
from app.forms import LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    params = {
        "title": "Authentication"
    }
    
    form = LoginForm()
    
    if form.validate_on_submit():
        return redirect(url_for("auth.success"))
    
    return render_template("login.html", **params, form=form)


@auth_bp.route("/success")
def success() -> str:
    return "<h1>Login Successful!</h1>"
