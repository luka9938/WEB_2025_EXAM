from bottle import default_app, run
import routes.items
import routes.auth
import routes.static
import routes.pages

application = default_app()

try:
    import production
    application = default_app()
except:
    run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0)
