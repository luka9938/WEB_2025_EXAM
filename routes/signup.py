from bottle import get, template, request, post, response
import utils.db
import x
import bcrypt
import utils.validation as valid
import utils.verification as verification
import icecream as ic
@get("/signup")
def _():
    try:
        return template("signup.html", **request.header_context)
    except Exception as ex:
        print("there was a problem loading the page")
        print(ex)
        return ex
    finally:
        pass

@post("/signup")
def signup():
    try:
        
        user_name = valid.validate_username()
        user_email = valid.validate_email()
        user_password = valid.validate_password()
        verification_code = verification.generate_verification_code()
        selected_option = request.forms.get("option")
        
        with utils.db.db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_email = ?", (user_email,))
            existing_user = cursor.fetchone()
        
        if existing_user:
            return "User already exists"
        
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        
        user = {
            "user_name": user_name, 
            "user_email": user_email, 
            "user_password": hashed_password.decode('utf-8'), 
            "user_role": selected_option, 
            "user_verification_code": verification_code,
            "user_is_blocked": False,
            "user_is_verified": True,
            "user_is_deleted": False
        }
        
        with utils.db.db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user_name, user_email, user_password, user_role, user_verification_code, user_is_blocked, user_is_verified, user_is_deleted) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user["user_name"], user["user_email"], user["user_password"], user["user_role"], 
                  user["user_verification_code"], user["user_is_blocked"],user["user_is_verified"], user["user_is_deleted"]))
            conn.commit()

        response.status = 303
        response.set_header('Location', '/login')
    except Exception as ex:
        ic(ex)
        if "user_name" in str(ex):
            return f"""
            <template mix-target="#message">
                {ex.args[1]}
            </template>
            """
    finally:
        if "db" in locals(): utils.db.db.close()