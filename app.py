import os

from server import app, db
from server import app
from flask_migrate import Migrate

migrate = Migrate(app, db, compare_type = True)

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 80)),
        debug=os.getenv("DEBUG", False),
    )
