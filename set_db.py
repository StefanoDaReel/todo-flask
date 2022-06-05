from todo_api import create_app, db
from todo_api.models import *


if __name__ == '__main__':
    app = create_app()
    db.create_all(app=app)
