from FreeTAKServer.core.persistence.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.User import User


class UserTableController(TableController):
    def __init__(self):
        self.table = User
