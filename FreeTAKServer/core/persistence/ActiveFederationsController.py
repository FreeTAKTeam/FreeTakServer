from FreeTAKServer.core.persistence.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.federations import ActiveFederations


class ActiveFederationsController(TableController):
    def __init__(self):
        self.table = ActiveFederations
