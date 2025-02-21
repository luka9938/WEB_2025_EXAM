import re
from bottle import request
import x

USER_ID_REGEX = "^[a-f0-9]{32}$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_role(expected_role):
    user_role = request.get_cookie("user_role", secret=x.COOKIE_SECRET)  # Use "user_role" instead of "role"
    return user_role == expected_role if user_role else False

##############################
EMAIL_MAX = 100
EMAIL_REGEX = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_email():
    error = f"email invalid"
    user_email = request.forms.get("user_email", "").strip()
    if not re.match(EMAIL_REGEX, user_email):
        raise Exception(error, 400)
    return user_email
##############################
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = "^[a-z]{2,20}$"

def validate_username():
    error = f"username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} lowercase english letters"
    user_username = request.forms.get("user_name", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username):
        raise Exception(error, 400)
    return user_username
##############################
USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_password = request.forms.get("user_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_password):
        raise Exception(error, 400)
    return user_password

##############################
def confirm_password():
    error = f"password and confirm_password do not match"
    user_password = request.forms.get("user_password", "").strip()
    user_confirm_password = request.forms.get("user_confirm_password", "").strip()
    if user_password != user_confirm_password:
        raise Exception(error, 400)
    return user_confirm_password

