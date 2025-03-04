from bottle import get, post, template, response, request
import utils.db as db_utils
from utils.random_string import generate_random_string
import os
UPLOAD_DIR = "images/uploads"

@get('/edit_item/<key>')
def edit_item_form(key):
    try:
        db_conn = db_utils.db()
        cursor = db_conn.cursor()

        cursor.execute("SELECT * FROM items WHERE item_pk = ?", (key,))
        item = cursor.fetchone()

        db_conn.close()

        if not item:
            response.status = 404
            return {"error": "Item not found"}

        title = f"Edit your property"
        return template("edit_item", key=key, title=title, item=item, **request.header_context)
    except Exception as ex:
        return str(ex)
    finally:
        if "db" in locals(): db_utils.db.close()

@post('/edit_item/<key>')
def update_item(key):
    try:
        item_name = request.forms.get('item_name')
        item_price_per_night = request.forms.get('item_price_per_night')
        
        item_splash_image = request.files.get('item_splash_image')
        image2 = request.files.get('item_image2')
        image3 = request.files.get('item_image3')

        db_conn = db_utils.db()
        cursor = db_conn.cursor()

        cursor.execute("SELECT * FROM items WHERE item_pk = ?", (key,))
        item = cursor.fetchone()
        if not item:
            response.status = 404
            return {"error": "Item not found"}

        # Process splash image
        splash_image_filename = item['item_splash_image']
        if item_splash_image and item_splash_image.filename:
            splash_image_filename = f"{generate_random_string()}_{item_splash_image.filename}"
            splash_image_path = os.path.join(UPLOAD_DIR, splash_image_filename)
            item_splash_image.save(splash_image_path)
            # Delete old image
            if item['item_splash_image']:
                old_image_path = os.path.join(UPLOAD_DIR, item['item_splash_image'])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        # Process additional images
        image2_filename = item['item_image2']
        if image2 and image2.filename:
            image2_filename = f"{generate_random_string()}_{image2.filename}"
            image2_path = os.path.join(UPLOAD_DIR, image2_filename)
            image2.save(image2_path)
            # Delete old image
            if item['item_image2']:
                old_image_path = os.path.join(UPLOAD_DIR, item['item_image2'])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        image3_filename = item['item_image3']
        if image3 and image3.filename:
            image3_filename = f"{generate_random_string()}_{image3.filename}"
            image3_path = os.path.join(UPLOAD_DIR, image3_filename)
            image3.save(image3_path)
            # Delete old image
            if item['item_image3']:
                old_image_path = os.path.join(UPLOAD_DIR, item['item_image3'])
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        cursor.execute("""
            UPDATE items SET 
            item_name = ?, 
            item_price_per_night = ?, 
            item_splash_image = ?, 
            item_image2 = ?, 
            item_image3 = ? 
            WHERE item_pk = ?
            """, (item_name, item_price_per_night, splash_image_filename, image2_filename, image3_filename, key))
        db_conn.commit()
        
        db_conn.close()

        response.status = 303
        response.set_header('Location', '/partner_properties')
        return
    except Exception as ex:
        return {"error": str(ex)}
    finally:
        if "db" in locals(): db_utils.db.close()