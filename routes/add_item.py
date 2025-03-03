from bottle import get, post, template, request, response
import utils.db as db_utils
import random
import os
import time
from utils.random_string import generate_random_string
import x
UPLOAD_DIR = "images/uploads"

@get("/add_item")
def add_item_form():
    """
    Serves the add_item.html template. This form is used to input
    the details of a new item and upload an image for the item.
    """
    try:
        return template("add_item.html", **request.header_context)
    except Exception as ex:
        print("There was a problem loading the page:", ex)
        return str(ex)

@post("/add_item")
def add_item():
    try:
        item_user = request.get_cookie("user_pk", secret=x.COOKIE_SECRET)
        item_email = request.get_cookie("user_email", secret=x.COOKIE_SECRET)
        # Get form data
        item_name = request.forms.get("item_name")
        
        # Generate random values for latitude, longitude, and stars
        item_lat = round(random.uniform(55.65, 55.7), 4)
        item_lon = round(random.uniform(12.55, 12.6), 4)
        item_stars = round(random.uniform(3.0, 5.0), 1)
        
        item_price_per_night = request.forms.get("item_price_per_night")

        # Process splash image
        item_splash_image = request.files.get("item_splash_image")

        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        # Generate random filename for splash image
        splash_image_filename = f"{generate_random_string()}_{item_splash_image.filename}"
    
        splash_image_path = os.path.join(UPLOAD_DIR, splash_image_filename)
        item_splash_image.save(splash_image_path)

        # Process additional images
        image2 = request.files.get("image2")
        image2_filename = f"{generate_random_string()}_{image2.filename}"
        image2_path = os.path.join(UPLOAD_DIR, image2_filename)
        image2.save(image2_path)
        
        image3 = request.files.get("image3")
        image3_filename = f"{generate_random_string()}_{image3.filename}"
        image3_path = os.path.join(UPLOAD_DIR, image3_filename)
        image3.save(image3_path)

        # Create item data
        item = {
            "item_pk": generate_random_string(),
            "item_name": item_name,
            "item_splash_image": splash_image_filename,
            "item_lat": item_lat,
            "item_lon": item_lon,
            "item_stars": item_stars,
            "item_price_per_night": int(item_price_per_night),
            "item_created_at": int(time.time()),
            "item_updated_at": 0,
            "item_image2": image2_filename,
            "item_image3": image3_filename,
            "item_user": item_user,
            "item_email": item_email

        }

        # Save item to the database
        insert_query = """
        INSERT INTO items 
        (item_pk, item_name, item_splash_image, item_lat, item_lon, item_stars, item_price_per_night,
        item_created_at, item_updated_at, item_image2, item_image3, item_user, item_email) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        conn = db_utils.db()
        cursor = conn.cursor()
        cursor.execute(insert_query, ( item["item_pk"], item["item_name"], item["item_splash_image"], item["item_lat"],
                                    item["item_lon"], item["item_stars"], item["item_price_per_night"],
                                    item["item_created_at"], item["item_updated_at"], item["item_image2"],
                                    item["item_image3"], item["item_user"], item["item_email"]))
        conn.commit()
        cursor.close()
        conn.close()

        response.status = 303
        response.set_header('Location', '/partner_properties')
        return
    except Exception as ex:
        print("An error occurred:", ex)
        return f"An error occurred: {str(ex)}"
    finally:
        if "db" in locals(): db_utils.db.close()