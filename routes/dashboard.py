from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app_factory import db
from forms.auth_forms import EnableTwoFactorForm
from models.user import LoginHistory
from utils.security import generate_qr_code_data_uri, generate_totp_secret, get_totp_uri, verify_totp

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    history = (
        LoginHistory.query.filter_by(user_id=current_user.id)
        .order_by(LoginHistory.logged_in_at.desc())
        .limit(5)
        .all()
    )
    return render_template("dashboard.html", history=history)


@dashboard_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@dashboard_bp.route("/2fa/setup", methods=["GET", "POST"])
@login_required
def setup_2fa():
    if not current_user.totp_secret:
        current_user.totp_secret = generate_totp_secret()
        db.session.commit()

    form = EnableTwoFactorForm()
    totp_uri = get_totp_uri(current_user)
    qr_code = generate_qr_code_data_uri(totp_uri)
    if form.validate_on_submit():
        if verify_totp(current_user.totp_secret, form.token.data):
            current_user.is_totp_enabled = True
            db.session.commit()
            flash("Two-factor authentication is now enabled.", "success")
            return redirect(url_for("dashboard.profile"))
        flash("Invalid authenticator code. Try the current code from your app.", "danger")

    return render_template("setup_2fa.html", form=form, totp_uri=totp_uri, qr_code=qr_code)


@dashboard_bp.route("/2fa/disable", methods=["POST"])
@login_required
def disable_2fa():
    current_user.is_totp_enabled = False
    current_user.totp_secret = None
    db.session.commit()
    flash("Two-factor authentication has been disabled.", "info")
    return redirect(url_for("dashboard.profile"))