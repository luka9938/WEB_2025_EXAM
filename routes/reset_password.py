from bottle import get, template, response, request
import utils.db as db_utils
import sqlite3
import icecream as ic

@get("/reset-password/<key>")
def reset_password(key):
    try:
        # Connect to the database and set row_factory to enable dictionary-like access
        with db_utils.db() as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT user_pk, user_name, user_email FROM users WHERE user_pk = ?", (key,))
            user_data = cursor.fetchone()

        if not user_data:
            response.status = 404
            return {"error": "User not found"}

        # Convert the row to a dictionary for template use
        user = dict(user_data)
        ic(user)
        
        return template("reset-password.html", key=key, user=user, **request.header_context)
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "db" in locals(): db.close()