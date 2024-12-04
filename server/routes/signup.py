import json

from flask import Blueprint, request, session
from server import db
from server.models.user import User
from server.models.login import Login
from server.models.key import Key
from server.utils.hash_salt import hash_salt_password

signup_route = Blueprint(
    "signup_route",
    __name__,
)

def same_username(username):
    return User.query.filter_by(username=username).scalar() is not None

@signup_route.route("/api/signup", methods=["POST"])
def sign_up():
    try:
        data = json.loads(request.data)
        username = data['username']
        password = data['password']
        publicPEM = data['public']
        privatePEM= data['private']
        if same_username(username):
            return {
                "success": False,
                "message": "Username, " + username + " has already taken. Please try another username"
            }
        
        user = User(username=username)
        login = Login(username=username, password=hash_salt_password(password))

        db.session.add(user)
        db.session.add(login)
        db.session.commit()
        
        key = Key(
            user_id = user.id,
            public = publicPEM,
            private = privatePEM
        )
        db.session.add(key)
        db.session.commit()

        session["id"] = user.id

        return {"success": True}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400
