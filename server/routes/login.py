import json

from flask import Blueprint, request, session
from server import db
from server.models.user import User
from server.models.login import Login
from server.models.key import Key
from server.utils.hash_salt import compare_plain_hash
from server.routes.signup import same_username

login_route = Blueprint(
    "login_route",
    __name__,
)

def get_pwd(username):
    query = db.session.query(Login).filter(Login.username == username).one()
    return query.password

def get_id(username):
    query = db.session.query(User).filter(User.username == username).one()
    return query.id

def get_private_key(user_id):
    query = db.session.query(Key).filter(Key.user_id == user_id).one()
    return query.private

@login_route.route("/api/login", methods=["POST"])
def login():
    try:
        data = json.loads(request.data)
        username = data['username']
        password = data['password']

        if (same_username(username) is False or compare_plain_hash(get_pwd(username),password) is False):
            return {
                "success": False,
                "message": "Username does not exist or password does not match username. Please try again."
            }
        
        session["id"] = get_id(username)
        encrypted_private_key = get_private_key(session["id"])

        return {
            "success": True,
            "encryptedKey": encrypted_private_key,
        }
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400
