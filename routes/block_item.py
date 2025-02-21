from bottle import post, request, response, template
import utils.db as db_utils
import icecream as ic
import x
import sqlite3

@post("/block_item/<key>")
def block_item(key):
    try:
        with db_utils.db() as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT item_blocked FROM items WHERE item_pk = ?", (key,))
            row = cursor.fetchone()
            if not row:
                return "Item not found"
            current_blocked = row["item_blocked"]
            
            # Toggle the blocked value: if blocked (1) then unblock (0), otherwise block (1)
            new_blocked = 0 if current_blocked else 1
            
            # Update the item with the new blocked status
            cursor.execute("UPDATE items SET item_blocked = ? WHERE item_pk = ?", (new_blocked, key))
            db.commit()
            
            # Retrieve the updated item
            cursor.execute("SELECT * FROM items WHERE item_pk = ?", (key,))
            updated_item = cursor.fetchone()
            
            # Extract the item's email
            
            # Send email based on the item's blocked status if email exists
        
        response.status = 303
        response.set_header('Location', '/')
        return

    except Exception as ex:
        ic(ex)
        return "An error occurred"
    finally:
        if "db" in locals(): db.close()
