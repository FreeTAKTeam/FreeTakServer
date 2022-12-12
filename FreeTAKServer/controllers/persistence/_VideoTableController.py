from FreeTAKServer.controllers.persistence.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.CoTTables._Video import _Video

class _VideoTableController(TableController):

    def __init__(self):
        self.table = _Video