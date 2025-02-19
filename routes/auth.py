from bottle import get, post, request, response, template
import utils.db as db_utils
import utils.validation as validation
import bcrypt
from icecream import ic
import x

@get("/login")
def _():
    x.no_cache()
    return template("login.html")

@post("/login")
def _():
    try:
        user_email = validation.validate_email()
        user_password = validation.validate_password()

        db = db_utils.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,))
        user = q.fetchone()
        if not user:
            raise Exception("User not found", 400)
        if not bcrypt.checkpw(user_password.encode(), user["user_password"].encode()):
            raise Exception("Invalid credentials", 400)

        user.pop("user_password")
        ic(user)

        response.set_cookie("user", user, secret=x.COOKIE_SECRET, httponly=True)
        return f'<template mix-redirect="/profile"></template>'
    except Exception as ex:
        ic(ex)
        response.status = 500
        return '<template mix-target="#toast"><div class="error">System under maintenance</div></template>'
    finally:
        if "db" in locals(): db.close()
