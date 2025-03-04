from bottle import post, request, response
import utils.db as db_utils
import bcrypt
import x
import icecream as ic

sessions = {}

@post("/update_profile")
def update_profile():
    try:
        
        # Restore session from cookies if missing
        user_pk = request.get_cookie("user_pk", secret=x.COOKIE_SECRET)
        user_email = request.get_cookie("user_email", secret=x.COOKIE_SECRET)
        user_role = request.get_cookie("user_role", secret=x.COOKIE_SECRET)

        # Rebuild session from cookies
        user = {
            "user_pk": user_pk,
            "user_email": user_email,
            "user_role": user_role
        }

        # Get the updated profile information from the form
        user_name = request.forms.get("user_name")
        user_email = request.forms.get("user_email")
        user_password = request.forms.get("user_password")

        # Hash the password if provided, else keep the old password
        if user_password:
            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            hashed_password = user["user_password"]

        # Update session data
        user["user_name"] = user_name
        user["user_email"] = user_email
        user["user_password"] = hashed_password
        
        db_conn = db_utils.db()
        cursor = db_conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET user_name = ?, user_email = ?, user_password = ?
            WHERE user_pk = ?
        """, (user_name, user_email, hashed_password, user["user_pk"]))
        db_conn.commit()

        # Set success message cookie
        response.set_cookie("success_message", "Profile updated successfully", path='/')

        # Redirect to profile page
        response.status = 303
        response.set_header('Location', '/profile')
        return

    except Exception as ex:
        ic(ex)
        return f"An error occurred: {ex}"

