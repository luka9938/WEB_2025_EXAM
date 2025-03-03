from bottle import get, request, response, template
import utils.db as db_utils
import x  # Ensure x.COOKIE_SECRET is properly set
import sqlite3

@get("/users")
def users():
    try:
        with db_utils.db() as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()

            # Fetch active users (not blocked)
            cursor.execute("SELECT user_pk, user_name, user_email FROM users WHERE user_blocked = false")
            active_users = cursor.fetchall()

            # Fetch blocked users
            cursor.execute("SELECT user_pk, user_name, user_email FROM users WHERE user_blocked = true")
            blocked_users = cursor.fetchall()

        # Convert results to dictionaries (prevents tuple-related errors)
        active_users = [dict(row) for row in active_users] if active_users else []
        blocked_users = [dict(row) for row in blocked_users] if blocked_users else []

        return template("users", active_users=active_users, blocked_users=blocked_users, **request.header_context)

    except Exception as ex:
        print("An error occurred:", ex)
        return {"error": str(ex)}
