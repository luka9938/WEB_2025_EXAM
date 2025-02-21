from bottle import get, template, request

@get("/add_item")
def add_item_form():
    try:
        return template("add_item.html", **request.header_context)
    except Exception as ex:
        print("There was a problem loading the page:", ex)
        return str(ex)