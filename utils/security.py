import base64
from io import BytesIO

from itsdangerous import URLSafeTimedSerializer
import pyotp
import qrcode
from flask import current_app, request


def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def generate_reset_token(email):
    return get_serializer().dumps(email, salt="password-reset")


def verify_reset_token(token, max_age=1800):
    try:
        return get_serializer().loads(token, salt="password-reset", max_age=max_age)
    except Exception:
        return None


def generate_totp_secret():
    return pyotp.random_base32()


def get_totp_uri(user):
    return pyotp.TOTP(user.totp_secret).provisioning_uri(name=user.email, issuer_name="Cyber Secure Login")


def generate_qr_code_data_uri(value):
    # QR is generated server-side so the TOTP secret is not sent to a third-party QR service.
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(value)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def verify_totp(secret, token):
    return pyotp.TOTP(secret).verify(token, valid_window=1)


def client_ip():
    # In production behind a trusted proxy, configure ProxyFix and trusted proxy headers carefully.
    return request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()


def sanitized_user_agent():
    return (request.headers.get("User-Agent") or "unknown")[:255]