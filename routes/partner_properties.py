from bottle import get, template, request
import utils.db as db_utils
import x
@get("/partner_properties")
def get_partner_properties():
    try:
        active_user = request.get_cookie("user_pk", secret=x.COOKIE_SECRET)
        if not active_user:
            return "User ID not found in cookies"

        # Query to fetch user's items from SQLite
        with db_utils.db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items WHERE user_pk = ?", (active_user,))
            your_items = cursor.fetchall()

        return template("partner_items.html", your_items=your_items, **request.header_context)

    except Exception as ex:
        # Handle any exceptions
        print("An error occurred:", ex)
        return str(ex)
    finally:
        if "db" in locals(): db_utils.db.close()