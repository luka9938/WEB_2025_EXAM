from bottle import get, template, response, request
import x
import credentials
import utils.validation as valid
from icecream import ic

@get("/")
def home():
    try:
        db = x.db()
        q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        items = q.fetchall()
        db.close()
        ic(items)
        try:
            is_customer = valid.validate_role("customer")
            is_partner = valid.validate_role("partner")
            is_admin = valid.validate_role("admin")

        except:
            pass

        return template("index.html", items=items, mapbox_token=credentials.mapbox_token, is_admin_role=is_admin, is_partner_role=is_partner, is_customer_role=is_customer, **request.header_context)
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "db" in locals(): db.close()
