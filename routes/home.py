from bottle import get, template, response
import x
import credentials
from icecream import ic

@get("/")
def home():
    try:
        db = x.db()
        q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        items = q.fetchall()
        db.close()
        ic(items)

        is_logged = False
        try:
            is_logged = x.validate_user()
        except:
            pass

        return template("index.html", items=items, mapbox_token=credentials.mapbox_token, is_logged=is_logged)
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        if "db" in locals(): db.close()

@get("/profile")
def profile():
    try:
        x.no_cache()
        x.validate_user_logged()
        db = x.db()
        q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        items = q.fetchall()
        return template("profile.html", is_logged=True, items=items)
    except Exception as ex:
        ic(ex)
        response.status = 303
        response.set_header('Location', '/login')
        return
    finally:
        if "db" in locals(): db.close()
