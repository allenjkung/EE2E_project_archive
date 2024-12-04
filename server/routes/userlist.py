from flask import session
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, session
from server import db
from server.models.user import User

userlist_route = Blueprint(
    "userlist_route",
    __name__,
)

def get_all_users():
    rows = db.session.query(User).all()
    return rows

@userlist_route.route("/api/userlist")
def get_user_list():
    try:
        users = get_all_users()
        users_data = []
        user_id = session["id"]
        fake_id = 1
        for user in users:
            if user_id is not user.id:
                users_data.append( {
                    "username": user.username,
                    "id": fake_id
                })
                fake_id += 1
        return {
            "users": users_data
        }
    except NoResultFound:
        return {"error": "Result not found"}, 404
