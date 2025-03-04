from bottle import default_app, run, request, hook
import routes.items
import routes.login
import routes.logout
import routes.static
import routes.index
import routes.profile
import routes.update_profile
import routes.rooms
import routes.users
import routes.add_item
import routes.reset_password
import routes.signup
import routes.partner_properties
import routes.block_item
import routes.block_user
import routes.toggle_booking
import routes.edit_item
import routes.delete_item
import routes.forgot_password
import routes.reset_password
import routes.delete_user
import utils.validation as valid


application = default_app()


# Function to build the header context
def build_header_context():
    return {
        "is_role": valid.validate_role("partner"),
        "is_admin_role": valid.validate_role("admin"),
        "is_customer_role": valid.validate_role("customer"),
        "is_logged": bool(request.get_cookie("user_session_id")),
    }

# Hook to make `header_context` available globally
@hook('before_request')
def add_header_context():
    request.header_context = build_header_context()

try:
    import production
    application = default_app()
except:
    run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0)
