from datetime import datetime, timedelta, timezone

from flask_login import UserMixin

from app_factory import db


def utcnow():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    last_login_at = db.Column(db.DateTime(timezone=True))
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    lockout_until = db.Column(db.DateTime(timezone=True))
    totp_secret = db.Column(db.String(32))
    is_totp_enabled = db.Column(db.Boolean, default=False, nullable=False)

    login_history = db.relationship("LoginHistory", backref="user", lazy=True, cascade="all, delete-orphan")

    def is_locked(self):
        return self.lockout_until is not None and self.lockout_until > utcnow()

    def register_failed_login(self, max_attempts=5, lockout_minutes=15):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= max_attempts:
            self.lockout_until = utcnow() + timedelta(minutes=lockout_minutes)

    def register_successful_login(self):
        self.failed_login_attempts = 0
        self.lockout_until = None
        self.last_login_at = utcnow()


class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    logged_in_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)