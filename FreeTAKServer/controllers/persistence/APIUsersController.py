from FreeTAKServer.controllers.persistence.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.APIUsers import APIUsers

class APIUsersController(TableController):

    def __init__(self):
        self.table = APIUsers