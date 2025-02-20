import re
from bottle import request
import x

USER_ID_REGEX = "^[a-f0-9]{32}$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
PASSWORD_REGEX = "^.{6,50}$"
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_role(expected_role):
    user_role = request.get_cookie("user_role", secret=x.COOKIE_SECRET)  # Use "user_role" instead of "role"
    return user_role == expected_role if user_role else False

# Usage examples:
is_partner = validate_role("partner")
is_admin = validate_role("admin")
is_customer = validate_role("customer")
