from bottle import post, response, request, template
import utils.db as db_utils
import icecream as ic
import sqlite3
import bcrypt
@post("/delete-user")
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
            return template("profile.html", error_message="Incorrect email or password", **request.header_context)

        stored_hashed_password = user["user_password"]
        if not stored_hashed_password or not bcrypt.checkpw(user_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            print("Password check failed for user:", user_email)
            return template("login.html", error_message="Your password is wrong", **request.header_context)

        cursor.execute("DELETE FROM users WHERE user_email = ?", (user_email,))
        cursor.execute("DELETE FROM items WHERE item_email = ?", (user_email,))
        conn.commit()
        conn.close()

        response.status = 303
        response.set_header('Location', '/')
        return

    except Exception as ex:
        # Handle any exceptions
        return str(ex)
    finally:
        if "db" in locals(): db_utils.db.close()