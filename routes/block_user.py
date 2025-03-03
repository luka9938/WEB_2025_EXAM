from bottle import post, response
import utils.db as db_utils
import icecream as ic
import sqlite3

@post("/block_user/<key>")
def block_user(key):
    try:
        with db_utils.db() as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT user_blocked FROM users WHERE user_pk = ?", (key,))
            row = cursor.fetchone()
            if not row:
                return "user not found"
            current_blocked = row["user_blocked"]
            
            # Toggle the blocked value: if blocked (1) then unblock (0), otherwise block (1)
            new_blocked = 0 if current_blocked else 1
            
            # Update the user with the new blocked status
            cursor.execute("UPDATE users SET user_blocked = ? WHERE user_pk = ?", (new_blocked, key))
            db.commit()
            
            # Retrieve the updated user
            cursor.execute("SELECT * FROM users WHERE user_pk = ?", (key,))
            updated_user = cursor.fetchone()
            
            # Extract the user's email
            
            # Send email based on the user's blocked status if email exists
        
        response.status = 303
        response.set_header('Location', '/users')
        return

    except Exception as ex:
        ic(ex)
        return "An error occurred"
    finally:
        if "db" in locals(): db.close()
