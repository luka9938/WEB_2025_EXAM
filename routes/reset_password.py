from bottle import get, put, template, response, request
import utils.db as db_utils
import bcrypt

@get("/reset-password/<key>")
def reset_password(key):
    try:
        db_conn = db_utils.db()
        cursor = db_conn.cursor()
        cursor.execute("SELECT user_pk, user_name, user_email FROM users WHERE user_pk = ?", (key,))
        user_data = cursor.fetchone()

        if not user_data:
            response.status = 404
            return {"error": "User not found"}

        user = dict(user_data)
        
        return template("reset-password.html", key=key, user=user, **request.header_context)
    except Exception as ex:
        return str(ex)
    finally:
        if "db" in locals(): db_utils.db.close()

@put("/reset-password/<key>")
def handle_reset_password(key):
    try:
        password = request.forms.get("password")
        confirm_password = request.forms.get("confirm_password")

        if password != confirm_password:
            return "Passwords do not match"
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        update_query = "UPDATE users SET user_password = ? WHERE user_pk = ?"
        db_conn = db_utils.db()
        cursor = db_conn.cursor()
        cursor.execute(update_query, (hashed_password, key))
        db_conn.commit()

        return "Password reset successfully"
    except Exception as ex:
        return str(ex)
    finally:
        if "db" in locals(): db_utils.db.close()