from server import app, db
from server.models.login import Login
from server.models.message import Message
from server.models.user import User

def query_table(table):
    if table == 1:
        rows = db.session.query(Login).all()
        for row in rows:
            print("username:", row.username, "\npassword:", row.password)
            print("----------")
    elif table == 2:
        rows = db.session.query(Message).all()
        for row in rows:
            print(row.id, row.username_to, row.username_from, row.message, row.time_sent)
    else:
        rows = db.session.query(User).all()
        for row in rows:
            print(row.id, row.username, row.registration_datetime)

def drop_table(table):
    if table == 1:
        Login.query.delete()
    elif table == 2:
        Message.query.delete()
    else:
        User.query.delete()

# query_table(2)
# drop_table(1)
#  
# 1 for login
# 2 for message
# 3 for user
