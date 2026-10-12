from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/masuk", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.is_active and user.check_password(password):
            login_user(user, remember=False, fresh=True)
            return redirect(url_for("admin.dashboard"))
        flash("Email atau kata sandi tidak valid.", "danger")
    return render_template("auth/login.html")


@auth_bp.post("/keluar")
def logout():
    logout_user()
    flash("Anda telah keluar.", "info")
    return redirect(url_for("public.index"))
