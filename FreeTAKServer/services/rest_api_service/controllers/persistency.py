from flask_sqlalchemy import SQLAlchemy

from FreeTAKServer.core.persistence.DatabaseController import DatabaseController

dbController = None

# TODO change everything about this
def init_config(app):
    global dbController
    db = SQLAlchemy(app)
    dbController = DatabaseController()
    dbController.session = db.session
