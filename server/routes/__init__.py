from flask import Blueprint, current_app, send_from_directory

from server.routes.signup import signup_route
from server.routes.login import login_route
from server.routes.userlist import userlist_route
from server.routes.message_input import message_input_route
from server.routes.get_messages import get_messages_route
from server.routes.key import key_route

main_route = Blueprint (
    "main_route",
    __name__,
)

@main_route.route("/", defaults={"filename": "index.html"})
@main_route.route("/<path:filename>")
def client(filename):
    print(current_app.template_folder)
    return send_from_directory(current_app.template_folder, filename)
