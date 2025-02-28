from bottle import post, request, response, template
import utils.db as db_utils
import icecream as ic
import x
import sqlite3

@post("/toggle_booking/<key>")
def block_item(key):
    try:
        with db_utils.db() as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT item_booked FROM items WHERE item_pk = ?", (key,))
            row = cursor.fetchone()
            if not row:
                return "Item not found"
            current_booked = row["item_booked"]
            
            # Toggle the booked value: if booked (1) then unblock (0), otherwise block (1)
            new_booked = 0 if current_booked else 1
            
            # Update the item with the new booked status
            cursor.execute("UPDATE items SET item_booked = ? WHERE item_pk = ?", (new_booked, key))
            db.commit()
            
            # Retrieve the updated item
            cursor.execute("SELECT * FROM items WHERE item_pk = ?", (key,))
            updated_item = cursor.fetchone()
            
            # Extract the item's email
            
            # Send email based on the item's booked status if email exists
        
        response.status = 303
        response.set_header('Location', f'/rooms/{key}')
        return

    except Exception as ex:
        ic(ex)
        return "An error occurred"
    finally:
        if "db" in locals(): db.close()

