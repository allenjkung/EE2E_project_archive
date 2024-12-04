import json

from flask import Blueprint, request, session
from server import db
from server.models.key import Key
from server.routes.login import get_id

key_route = Blueprint(
    "key_route",
    __name__,
)

def get_user_public_key(user_id):
    query = db.session.query(Key).filter(Key.user_id == user_id).one()
    return query.public

@key_route.route("/api/localkey", methods=["POST"])
def store_local_key():
    try:
        data = json.loads(request.data)
        private_key = data['private']
        session['private_key'] = private_key
        return {"success": True}

    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@key_route.route("/api/getkey", methods=["GET"])
def get_private_key():
    if 'private_key' not in session:
        return {"success": False, "message": "User is not suppose to be here."}
    return {"success": True, "private": session['private_key']}

@key_route.route("/api/getpublic", methods=["POST"])
def get_public_key():
    try:
        data = json.loads(request.data)
        username = data['to']
        user_id = get_id(username)
        public_key_user = get_user_public_key(user_id)
        public_key_self = get_user_public_key(session["id"])
        return {
            "success": True,
            "public_key_user": public_key_user,
            "public_key_self": public_key_self
        }
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400
