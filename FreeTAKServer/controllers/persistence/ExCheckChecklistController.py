from FreeTAKServer.controllers.DatabaseControllers.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.ExCheckChecklist import ExCheckChecklist

class ExCheckChecklistController(TableController):
    def __init__(self):
        self.table = ExCheckChecklist