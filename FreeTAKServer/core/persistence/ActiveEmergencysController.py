from FreeTAKServer.core.persistence.table_controllers import TableController
from FreeTAKServer.core.persistence.EventTableController import EventTableController
from FreeTAKServer.model.SQLAlchemy.ActiveEmergencys import ActiveEmergencys
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import make_transient


class ActiveEmergencysController(TableController):
    def __init__(self):
        self.table = ActiveEmergencys
    
    def create(self, session, object):

        try:
            row = ActiveEmergencys()
            row.event = EventTableController().convert_model_to_row(object, row.event)
            session.add(row)
            session.commit()
            return row
        except IntegrityError as e:
            from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
            try:
                session.rollback()
                session.close()
                db = DatabaseController()
                objold = db.query_CoT(f'uid = "{object.uid}"')[0]
                newobj = db.EventTableController.convert_model_to_row(object)
                x = objold.User
                db.session.delete(objold)
                db.session.commit()
                #make_transient(obj)
                newobj.User = x
                row.event = newobj
                db.session.add(row)
                db.session.commit()
            except Exception as e:
                raise e
        except Exception as e:
            session.rollback()
