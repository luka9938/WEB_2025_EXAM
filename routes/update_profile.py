from bottle import put, request, response
import utils.db as db_utils
import bcrypt
import x  # Make sure you have x.COOKIE_SECRET set for cookie secrets

sessions = {}

@put("/update_profile")
def update_profile():
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

        # Update the database
        with db_utils.db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users 
                SET user_name = ?, user_email = ?, user_password = ?
                WHERE user_pk = ?
            """, (user_name, user_email, hashed_password, user["user_pk"]))
            conn.commit()

        # Update session with the latest data
        sessions[user_session_id] = user

        # Set success message cookie
        response.set_cookie("success_message", "Profile updated successfully", path='/')

        # Redirect to profile page
        response.status = 303
        response.set_header('Location', '/profile')
        return

    except Exception as ex:
        print("An error occurred:", ex)
        return f"An error occurred: {ex}"

