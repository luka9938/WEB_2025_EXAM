from bottle import get, template, request
import utils.validation as utils_valid
import utils.db as db_utils
import credentials
import x

@get("/")
def _():
    try:
        db = db_utils.db()
        q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        items = q.fetchall()
        db.close()

        return template("index.html", items=items, mapbox_token=credentials.mapbox_token, **request.header_context)
    except Exception as ex:
        return str(ex)
