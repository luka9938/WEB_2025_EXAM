from bottle import get, static_file

@get("/app.css")
def _():
    return static_file("app.css", ".")

@get("/<file_name>.js")
def _(file_name):
    return static_file(file_name+".js", ".")

@get("/images/<item_splash_image>")
def _(item_splash_image):
    return static_file(item_splash_image, "images")
