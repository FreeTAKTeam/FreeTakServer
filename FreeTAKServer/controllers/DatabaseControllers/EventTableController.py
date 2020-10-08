from FreeTAKServer.controllers.DatabaseControllers.TableController import TableController
from FreeTAKServer.model.SQLAlchemy.Event import Event
import importlib

class EventTableController(TableController):
    def __init__(self):
        self.table = Event

    def create(self, session, object):
        row = self.convert_model_to_row(modelObject=object)
        session.add(row)
        session.commit()

    def convert_model_to_row(self, modelObject, rowObject = None):
        # TODO: find a more elegant way of doing this
        if rowObject == None:
            rowObject = Event()
        else:
            pass
        for attribName, attribValue in modelObject.__dict__.items():
            if hasattr(attribValue, '__dict__'):
                if attribName[0].isalpha():
                    pass
                else:
                    attribName[1].capitalize()
                subRowObjectImport = importlib.import_module(
                    f'FreeTAKServer.model.SQLAlchemy.CoTTables.{attribName.capitalize()}')
                subRowObject = getattr(subRowObjectImport, attribName.capitalize())()
                subTableRowObject = self.convert_model_to_row(attribValue, subRowObject)
                setattr(rowObject, attribName, subTableRowObject)

            elif isinstance(attribValue, list):
                if attribName[0].isalpha():
                    pass
                else:
                    attribName[1].capitalize()
                subRowObjectImport = importlib.import_module(
                    f'FreeTAKServer.model.SQLAlchemy.CoTTables.{attribName.capitalize()}')
                for element in attribValue:
                    subRowObject = getattr(subRowObjectImport, attribName.capitalize())()
                    subTableRowObject = self.convert_model_to_row(element, subRowObject)
                    setattr(subTableRowObject, "owner", rowObject)

            else:
                setattr(rowObject, attribName, attribValue)
        return rowObject