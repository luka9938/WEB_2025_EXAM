from bottle import post, response
import utils.db as db_utils
@post("/delete_item/<item_pk>")
def delete_item(item_pk):
    try:
        # Connect to the SQLite database
        conn = db_utils.db()
        cursor = conn.cursor()

        # Delete the item from SQLite
        cursor.execute("DELETE FROM items WHERE item_pk = ?", (item_pk,))
        conn.commit()
        conn.close()

        # Redirect to the partner properties page
        response.status = 303
        response.set_header('Location', '/partner_properties')
        return

    except Exception as ex:
        # Handle any exceptions
        return str(ex)
    finally:
        if "db" in locals(): db_utils.db.close()