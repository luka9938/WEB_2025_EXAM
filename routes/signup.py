from bottle import get, template, request, post, response
import utils.db
import bcrypt
import utils.validation as valid
import utils.verification as verification

@get("/signup")
def _():
    try:
        return template("signup.html", **request.header_context)
    except Exception as ex:
        print("There was a problem loading the page:", ex)
        return str(ex)

@post("/signup")
def signup():
    try:
        user_name = valid.validate_username()
        user_email = valid.validate_email()
        user_password = valid.validate_password()
        verification_code = verification.generate_verification_code()
        selected_option = request.forms.get("option")

        conn = utils.db.db()  # Get database connection
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_email = ?", (user_email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            return "User already exists"

        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = {
            "user_name": user_name, 
            "user_email": user_email, 
            "user_password": hashed_password, 
            "user_role": selected_option, 
            "user_verification_code": verification_code,
            "user_blocked": False,
            "user_verified": True,
            "user_deleted": False,
        }

        cursor.execute("""
            INSERT INTO users (user_name, user_email, user_password, user_role, user_verification_code, user_blocked, user_verified, user_deleted) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user["user_name"], user["user_email"], user["user_password"], user["user_role"], 
              user["user_verification_code"], user["user_blocked"], user["user_verified"], user["user_deleted"]))
        conn.commit()

        response.status = 303
        response.set_header('Location', '/login')

    except Exception as ex:
        print("Signup Error:", ex)
        return f"An error occurred: {str(ex)}"

    finally:
        if 'conn' in locals():
            conn.close()
