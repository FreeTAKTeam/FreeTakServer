from FreeTAKServer.controllers.DatabaseControllers.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.APICalls import APICalls

class APICallController(TableController):

    def __init__(self):
        self.table = APICalls