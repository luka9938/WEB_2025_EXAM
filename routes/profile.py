from bottle import response, request, get, template
import utils.validation as utils_valid
import utils.db as db_utils
import sqlite3

sessions = {}
@get("/profile")
def profile():
    try:
        user_session_id = request.get_cookie("user_session_id")
        if not user_session_id:
            response.status = 303
            response.set_header('Location', '/login')
            return

        if user_session_id not in sessions:
            response.status = 303
            response.set_header('Location', '/login')
            return

        user = sessions[user_session_id]
        is_logged = utils_valid.validate_user_logged()

        db = db_utils.db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user['user_id'],))
        user_data = cursor.fetchone()
        db.close()

        if not user_data:
            return "User not found"

        user_data = {
            'user_id': user_data[0],
            'username': user_data[1],
            'user_email': user_data[2],
            'user_password': user_data[3]
        }

        success_message = request.get_cookie("success_message")
        response.delete_cookie("success_message", path='/')

        return template("profile.html", user=user_data, is_logged=is_logged, success_message=success_message)
    except Exception as ex:
        print("An error occurred:", ex)
        return {"error": str(ex)}
    finally:
        if "db" in locals(): db.close()