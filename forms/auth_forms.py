import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError


PASSWORD_RULES = [
    (r"[A-Z]", "at least one uppercase letter"),
    (r"[a-z]", "at least one lowercase letter"),
    (r"\d", "at least one number"),
    (r"[^A-Za-z0-9]", "at least one special character"),
]


def strong_password(form, field):
    missing = [message for pattern, message in PASSWORD_RULES if not re.search(pattern, field.data or "")]
    if missing:
        raise ValidationError("Password must include " + ", ".join(missing) + ".")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(r"^[A-Za-z0-9_.-]+$", message="Use letters, numbers, dots, underscores, or hyphens only."),
        ],
    )
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8), strong_password])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")


class TwoFactorForm(FlaskForm):
    token = StringField("Authenticator Code", validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Verify")


class RequestResetForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired(), Length(min=8), strong_password])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")


class EnableTwoFactorForm(FlaskForm):
    token = StringField("Authenticator Code", validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Enable 2FA")