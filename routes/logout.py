from bottle import response, request, get

sessions = {}

@get("/logout")
def logout():
    try:
        user_session_id = request.get_cookie("user_session_id")
        if user_session_id and user_session_id in sessions:
            del sessions[user_session_id]

        response.delete_cookie("user_session_id")
        response.delete_cookie("user_role")
        response.delete_cookie("user_email")
        response.delete_cookie("user_pk")
        response.status = 303
        response.set_header('Location', '/')
        return
    except Exception as ex:
        print("An error occurred during logout:", ex)
        return "An error occurred during logout."

