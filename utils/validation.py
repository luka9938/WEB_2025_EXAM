import re
from bottle import request
import x

USER_ID_REGEX = "^[a-f0-9]{32}$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORD_REGEX = "^.{6,50}$"
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_user_logged():
    user = request.get_cookie("user_session_id")
    if user is None:
        return True
    else:
        return False

def validate_email():
    email = request.forms.get("user_email", "").strip()
    if not re.match(EMAIL_REGEX, email):
        raise Exception("Invalid email", 400)
    return email

def validate_password():
    password = request.forms.get("user_password", "").strip()
    if not re.match(PASSWORD_REGEX, password):
        raise Exception("Invalid password length", 400)
    return password
