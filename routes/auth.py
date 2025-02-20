from bottle import get, post, request, response, template, redirect
import utils.db as db_utils
import utils.validation as valid
import bcrypt
import uuid
import json
import x  # Ensure you have x.COOKIE_SECRET
import sqlite3

sessions = {}
@get("/login")
def login_get():
    return template("login.html", error_message=None, **request.header_context)

@post("/login")
def login_post():
    user_email = request.forms.get("user_email")
    user_password = request.forms.get("user_password")

    try:
        conn = db_utils.db()
        print("Database connection established.")
        conn.row_factory = sqlite3.Row  # Ensure dict-like access
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_email = ?", (user_email,))
        user = cursor.fetchone()
        print("Query result:", user)

        if not user:
            print("No user found with email:", user_email)
            return template("login.html", error_message="Incorrect email or password", **request.header_context)
        
        if not bool(user["user_is_verified"]):
            print("User not verified:", user_email)
            return template("login.html", error_message="Only verified users can login", **request.header_context)

        stored_hashed_password = user["user_password"]
        if not stored_hashed_password or not bcrypt.checkpw(user_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            print("Password check failed for user:", user_email)
            return template("login.html", error_message="Your password is wrong", **request.header_context)

        user_session_id = str(uuid.uuid4())
        sessions[user_session_id] = dict(user)  # Convert to dict if needed

        cookie_secret = x.COOKIE_SECRET
        print("Setting cookies:")
        print(f"user_session_id: {user_session_id}")
        print(f"user_role: {user['user_role']}")
        print(f"user_pk: {user['user_pk']}")
        print(f"user_email: {user_email}")

        response.set_cookie("user_session_id", user_session_id)
        response.set_cookie("user_role", user["user_role"], secret=cookie_secret)
        response.set_cookie("user_pk", str(user["user_pk"]), secret=cookie_secret)
        response.set_cookie("user_email", user_email, secret=cookie_secret)

        print(f"Sessions after login: {sessions}")
        
        response.status = 303
        response.set_header('Location', '/')
        return
    
    except Exception as ex:
        print("An error occurred during login:", ex)
        return template("login.html", error_message="An error occurred during login. Please try again.", **request.header_context)
    
    finally:
        if 'conn' in locals():
            conn.close()



@get("/logout")
def logout():
    try:
        user_session_id = request.get_cookie("user_session_id")
        if user_session_id and user_session_id in sessions:
            del sessions[user_session_id]

        response.delete_cookie("user_session_id")
        response.delete_cookie("user_role")
        response.delete_cookie("user_email")
        response.delete_cookie("user_pk")
        response.status = 303
        response.set_header('Location', '/')
        return
    except Exception as ex:
        print("An error occurred during logout:", ex)
        return "An error occurred during logout."

