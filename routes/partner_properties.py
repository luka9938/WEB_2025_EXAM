from bottle import get, template, request
import utils.db as db_utils
import x

@get("/partner_properties")
def get_partner_properties():
    try:
        active_user = request.get_cookie("user_pk", secret=x.COOKIE_SECRET)
        if not active_user:
            return "User ID not found in cookies"

        with db_utils.db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM items WHERE item_user = ?", (active_user,))
            your_items = cursor.fetchall()

        # If no items are found, ensure your_items is an empty list.
        your_items = your_items if your_items else []
        return template("partner_items.html", your_items=your_items, **request.header_context)

    except Exception as ex:
        print("An error occurred:", ex)
        return str(ex)
