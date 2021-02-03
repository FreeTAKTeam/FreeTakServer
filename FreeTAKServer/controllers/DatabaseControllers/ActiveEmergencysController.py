from FreeTAKServer.controllers.DatabaseControllers.table_controllers import TableController
from FreeTAKServer.controllers.DatabaseControllers.EventTableController import EventTableController
from FreeTAKServer.model.SQLAlchemy.ActiveEmergencys import ActiveEmergencys


class ActiveEmergencysController(TableController):
    def __init__(self):
        self.table = ActiveEmergencys

    def create(self, session, object):
        row = ActiveEmergencys()
        row.event = EventTableController().convert_model_to_row(object, row.event)
        session.add(row)
        session.commit()
        return row


if __name__ == "__main__":
    # TODO: This is broken. SimulateSentCOT() does not exist.
    modelObject = SimulateSentCoT().createFullObj()
    # DatabaseController().create_engine()
    # session = DatabaseController().create_Session()
    # row = ActiveEmergencysController().create(session, modelObject)
    # ActiveEmergencysController().delete(session, row)
