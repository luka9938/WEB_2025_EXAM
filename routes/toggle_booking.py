from bottle import post, request, template
import utils.db as db_utils
import sqlite3

@post("/toggle_booking")
def toggle_booking():
    try:
        item_pk = request.forms.get("item_pk")
        if not item_pk:
            return "Item ID not provided"

        # Connect to the database and set row factory for dict-like access
        with db_utils.db() as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            # Fetch the current booking status of the item
            cursor.execute("SELECT * FROM items WHERE item_pk = ?", (item_pk,))
            item = cursor.fetchone()
            if not item:
                return "Item not found"
            
            # Toggle the booking status
            current_booking_status = bool(item["is_booked"])
            new_booking_status = 0 if current_booking_status else 1
            
            # Update the booking status
            cursor.execute("UPDATE items SET is_booked = ? WHERE item_pk = ?", (new_booking_status, item_pk))
            db.commit()
            
            # Fetch the updated item
            cursor.execute("SELECT * FROM items WHERE item_pk = ?", (item_pk,))
            updated_item = cursor.fetchone()
        
        # Pass the updated item (converted to a dict) to the template.
        return template("rooms", id=item_pk, title=f"Item {item_pk}", item=dict(updated_item), **request.header_context)
    except Exception as ex:
        print("An error occurred:", ex)
        return str(ex)
