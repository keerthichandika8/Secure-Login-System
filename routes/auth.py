from flask import Blueprint, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_user, logout_user

from app_factory import bcrypt, db
from forms.auth_forms import LoginForm, RegisterForm, RequestResetForm, ResetPasswordForm, TwoFactorForm
from models.user import LoginHistory, User
from utils.security import client_ip, generate_reset_token, sanitized_user_agent, verify_reset_token, verify_totp

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        username = form.username.data.strip()

        if User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
            return render_template("register.html", form=form)

        # bcrypt salts every hash automatically, so equal passwords still produce different hashes.
        password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now sign in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        # Generic message prevents account enumeration.
        generic_error = "Invalid email or password."
        if not user:
            flash(generic_error, "danger")
            return render_template("login.html", form=form)

        if user.is_locked():
            flash("Too many failed attempts. Please try again later.", "danger")
            return render_template("login.html", form=form)

        if not bcrypt.check_password_hash(user.password_hash, form.password.data):
            user.register_failed_login()
            db.session.commit()
            flash(generic_error, "danger")
            return render_template("login.html", form=form)

        if user.is_totp_enabled:
            session.clear()
            session["pending_2fa_user_id"] = user.id
            session["remember_login"] = bool(form.remember.data)
            flash("Enter your authenticator code to finish signing in.", "info")
            return redirect(url_for("auth.verify_2fa"))

        complete_login(user, remember=form.remember.data)
        flash("Login successful. Welcome back.", "success")
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html", form=form)


@auth_bp.route("/verify-2fa", methods=["GET", "POST"])
def verify_2fa():
    user_id = session.get("pending_2fa_user_id")
    if not user_id:
        return redirect(url_for("auth.login"))

    user = db.session.get(User, user_id)
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    form = TwoFactorForm()
    if form.validate_on_submit():
        if verify_totp(user.totp_secret, form.token.data):
            remember = session.pop("remember_login", False)
            session.pop("pending_2fa_user_id", None)
            complete_login(user, remember=remember)
            flash("Two-factor verification complete.", "success")
            return redirect(url_for("dashboard.dashboard"))
        flash("Invalid or expired authenticator code.", "danger")

    return render_template("verify_2fa.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    session.clear()
    flash("You have been signed out securely.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = RequestResetForm()
    reset_link = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user:
            token = generate_reset_token(user.email)
            reset_link = url_for("auth.reset_password", token=token, _external=True)
        flash("If that email exists, a reset link has been prepared.", "info")
    return render_template("forgot_password.html", form=form, reset_link=reset_link)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("The password reset link is invalid or expired.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.failed_login_attempts = 0
        user.lockout_until = None
        db.session.commit()
        flash("Password reset successful. Please sign in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html", form=form)


def complete_login(user, remember=False):
    user.register_successful_login()
    history = LoginHistory(user=user, ip_address=client_ip(), user_agent=sanitized_user_agent())
    db.session.add(history)
    db.session.commit()
    session.permanent = True
    login_user(user, remember=remember)