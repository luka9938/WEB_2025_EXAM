from bottle import get, template, request, response
import utils.db as db_utils
import sqlite3

@get("/rooms/<id>")
def get_room(id):
    try:

        # Establish connection to SQLite database
        conn = db_utils.db()
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row  # To access columns by name

        # Execute SQL query to retrieve item with the given ID
        cursor.execute("SELECT * FROM items WHERE item_pk = ?", (id,))
        item = cursor.fetchone()

        # Close the database connection
        conn.close()

        # If item is not found, return 404 error
        if not item:
            response.status = 404
            return {"error": "Item not found"}

        # Convert sqlite3.Row to a dict
        item_dict = dict(item)

        # Calculate formatted price
        price = int(item_dict["item_price_per_night"])
        formatted_price = "{:,.0f}".format(price).replace(",", ".")

        # Prepare data for template rendering
        title = f"Item {id}"

        # Render the template with the retrieved item and other data
        return template("rooms",
                        id=id,
                        title=title,
                        item=item_dict,
                        formatted_price=formatted_price,**request.header_context)
    except Exception as ex:
        print("An error occurred:", ex)
        return {"error": str(ex)}
    finally:
        if "db" in locals(): db_utils.db.close()