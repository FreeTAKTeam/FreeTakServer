from FreeTAKServer.core.persistence.table_controllers import TableController
from FreeTAKServer.components.extended.excheck.persistence.ExCheckChecklist import ExCheckChecklist

class ExCheckChecklistController(TableController):
    def __init__(self):
        self.table = ExCheckChecklist