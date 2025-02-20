from bottle import get, request, response, template
import utils.db as db_utils
import x  # Ensure x.COOKIE_SECRET is properly set
import sqlite3

@get("/users")
def users():
    try:
        # Retrieve session ID from cookie
        user_session_id = request.get_cookie("user_session_id")
        if not user_session_id:
            print("No session ID found. Redirecting to login.")
            response.status = 303
            response.set_header('Location', '/login')
            return

        # Restore session from cookies
        user_pk = request.get_cookie("user_pk", secret=x.COOKIE_SECRET)
        user_email = request.get_cookie("user_email", secret=x.COOKIE_SECRET)
        user_role = request.get_cookie("user_role", secret=x.COOKIE_SECRET)

        if not user_pk or not user_email or not user_role:
            print("Incomplete session data in cookies. Redirecting to login.")
            response.status = 303
            response.set_header('Location', '/login')
            return
        
        # Ensure the user is an admin
        if user_role != "admin":
            print("Unauthorized access attempt by:", user_email)
            response.status = 403  # Forbidden
            return "Access denied. Admins only."

        # Connect to the database
        with db_utils.db() as db:
            db.row_factory = sqlite3.Row  # Enables dictionary-like row access
            cursor = db.cursor()

            # Fetch active users (not blocked)
            cursor.execute("SELECT user_pk, user_name, user_email FROM users WHERE user_is_blocked = 0")
            active_users = cursor.fetchall()

            # Fetch blocked users
            cursor.execute("SELECT user_pk, user_name, user_email FROM users WHERE user_is_blocked = 1")
            blocked_users = cursor.fetchall()

        # Convert results to dictionaries (prevents tuple-related errors)
        active_users = [dict(row) for row in active_users] if active_users else []
        blocked_users = [dict(row) for row in blocked_users] if blocked_users else []

        return template("users", active_users=active_users, blocked_users=blocked_users, **request.header_context)

    except Exception as ex:
        print("An error occurred:", ex)
        return {"error": str(ex)}
