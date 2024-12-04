import json

from server import db
from flask import Blueprint, request, session
from server.models.user import User
from server.models.message import Message

message_input_route = Blueprint(
    "message_input_route",
    __name__,
)

def get_username(id):
    query = db.session.query(User).filter(User.id == id).one()
    return query.username

def get_messages_history(original, username1, username2):
    query_all = db.session.query(Message).all()
    filtered_query = []
    for row in query_all:
        if ((row.original == original) and 
        ((row.username_to == username1 and row.username_from == username2) or 
        (row.username_to == username2 and row.username_from == username1))):
            filtered_query.append({
                "id": row.id,
                "username_from": row.username_from,
                "message": row.message.decode('utf-8')
            })
    return filtered_query

@message_input_route.route("/api/message/input", methods=["POST"])
def add_message():
    try:
        data = json.loads(request.data)
        user_to = data['to']
        message_self = data['message_self']
        message_to = data['message_to']
        encode_self = message_self.encode('utf-8')
        encode_to = message_to.encode('utf-8')
        if len(message_self) > 2048 or len(message_to) > 2048:
            return {
                "success": False,
                "message": "Message exceeds 2048 character limit."
            }
        user_from = get_username(session["id"])
        
        message_self = Message(
            original = user_from,
            username_to = user_to,
            username_from = user_from,
            message = encode_self
        )
        message_to = Message(
            original = user_to,
            username_to = user_to,
            username_from = user_from,
            message = encode_to
        )
        db.session.add(message_self)
        db.session.add(message_to);
        db.session.commit()
        
        nMessages = get_messages_history(user_from ,user_from, user_to)

        return {
            "success": True, 
            "messages": nMessages
        }
    except json.decoder.JSONDecoderError:
        return {"error": "Malformed request"}, 400
