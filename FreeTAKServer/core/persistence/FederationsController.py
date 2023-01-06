from FreeTAKServer.core.persistence.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.federations import Federations


class FederationsController(TableController):
    def __init__(self):
        self.table = Federations
