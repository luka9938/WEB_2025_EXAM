from bottle import get, post, template, request
import utils.db as db_utils
import utils.email_service as email_utils
import icecream as ic

@get("/forgot-password")
def forgot_password():
    return template("forgot-password.html", **request.header_context)

##############################
@post("/forgot-password")
def handle_forgot_password():
    try:
        email = request.forms.get("user_email")
        db_conn = db_utils.db()
        cursor = db_conn.cursor()
        # Query user from SQLite database
        user_query = "SELECT * FROM users WHERE user_email = ?"
        result = cursor.execute(user_query, (email,))
        user = result.fetchone()

        if not user:
            raise Exception("Email not found")

        # Extract user data and send reset email
        user_pk = user["user_pk"]
        email_utils.send_reset_email(email, user_pk)

        return "Password reset email sent"
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "db" in locals(): db_utils.db.close()