from bottle import get, request, response, template
import utils.db as db_utils
import x
@get("/profile")
def profile():
    try:
        # Retrieve session ID from cookie
        user_session_id = request.get_cookie("user_session_id")
        if not user_session_id:
            print("No session ID found. Redirecting to login.")
            response.status = 303
            response.set_header('Location', '/login')
            return
        
        # Restore session from cookies if missing
        user_pk = request.get_cookie("user_pk", secret=x.COOKIE_SECRET)
        user_email = request.get_cookie("user_email", secret=x.COOKIE_SECRET)
        user_role = request.get_cookie("user_role", secret=x.COOKIE_SECRET)

        if not user_pk or not user_email or not user_role:
            print("Incomplete session data in cookies. Redirecting to login.")
            response.status = 303
            response.set_header('Location', '/login')
            return

        # Rebuild session from cookies
        user = {
            "user_pk": user_pk,
            "user_email": user_email,
            "user_role": user_role
        }

        # Fetch user data from database
        with db_utils.db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_pk, user_name, user_email FROM users WHERE user_pk = ?", (user["user_pk"],))
            user_data = cursor.fetchone()

        success_message = request.get_cookie("success_message", default=None)
        if success_message:
            response.delete_cookie("success_message", path='/')

        return template("profile.html", user=user_data, success_message=success_message, error_message=None, **request.header_context)

    except Exception as ex:
        print("An error occurred in profile:", ex)

    finally:
        if "db" in locals(): db.close()
