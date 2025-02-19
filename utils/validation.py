import re
from bottle import request, response
import x

USER_ID_REGEX = "^[a-f0-9]{32}$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORD_REGEX = "^.{6,50}$"
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_user_logged():
    user = request.get_cookie("user", secret=x.COOKIE_SECRET)
    if user is None:
        raise Exception("User must log in", 400)
    return user

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
