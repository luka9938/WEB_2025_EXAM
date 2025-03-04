from bottle import get, template, request
import utils.db as db_utils
import json
import x

@get("/items/page/<page_number>")
def _(page_number):
    try:
        db = db_utils.db()
        next_page = int(page_number) + 1
        offset = (int(page_number) - 1) * x.ITEMS_PER_PAGE
        q = db.execute("SELECT * FROM items ORDER BY item_created_at LIMIT ? OFFSET ?", (x.ITEMS_PER_PAGE, offset))
        items = q.fetchall()

        html = "".join([template("_item", item=item, **request.header_context) for item in items])
        btn_more = template("__btn_more", page_number=next_page) if len(items) >= x.ITEMS_PER_PAGE else ""

        return f"""
        <template mix-target="#items" mix-bottom>{html}</template>
        <template mix-target="#more" mix-replace>{btn_more}</template>
        <template mix-function="test">{json.dumps(items)}</template>
        """
    except Exception as ex:
        return "ups..."
    finally:
        if "db" in locals(): db.close()
