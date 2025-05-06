from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm, SignUpForm
from app.services import create_user, check_if_user_exists

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    params = {
        "title": "Log in"
    }
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = check_if_user_exists(email=form.username.data, username=form.username.data)
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
                               message="Incorrect email/username or password",
                               form=form)
    return render_template("login.html", **params, form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup() -> str:
    params = {
        "title": "Sign up"
    }
    
    form = SignUpForm()
    
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template("signup.html", **params, form=form,
                                   message="Passwords do not match")
        
        if check_if_user_exists(email=form.email.data, username=form.username.data):
            return render_template("signup.html", **params, form=form,
                                   message="This user already exists")
     
        user = create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            bio=form.bio.data
        )
        
        user = check_if_user_exists(email=form.email.data, username=form.username.data)
        login_user(user, remember=True)
        
        return redirect("/")
    return render_template("signup.html", **params, form=form)


@auth_bp.route("/logout")
@login_required
def logout() -> None:
    logout_user()
    return redirect("/")
