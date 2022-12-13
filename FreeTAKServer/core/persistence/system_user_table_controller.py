from FreeTAKServer.core.persistence.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.system_user import SystemUser

class SystemUserTableController(TableController):
    def __init__(self):
        self.table = SystemUser