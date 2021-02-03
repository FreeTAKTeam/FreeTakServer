from sqlalchemy import text

from FreeTAKServer.model.SQLAlchemy.User import User

from FreeTAKServer.model.SQLAlchemy.federations import ActiveFederations
from FreeTAKServer.model.SQLAlchemy.federations import Federations


class TableController:
    # default constructor  def __init__(self):
    table = None

    def delete(self, session, query):
        # this function removes a row from the specified table based on the query
        objs_to_be_deleted = session.query(self.table).filter(text(query)).all()
        if objs_to_be_deleted:
            for obj_to_be_deleted in objs_to_be_deleted:
                session.delete(obj_to_be_deleted)
            session.commit()
        else:
            return None
        return 1

    def create(self, session, **args):
        # this function adds a new row to the datapackages table
        newobj = self.table(**args)
        session.add(newobj)
        session.commit()

    def query(self, session, query, columns):
        # query needs to be applicable to datapackage object tuple(['DataPackage.'+x for x in columns])
        output = session.query(*tuple([getattr(self.table, x) if x != '*' else self.table for x in columns])).filter(
            text(query)).all()
        return output

    def update(self, session, query, column_value):
        DataPackages = session.query(self.table).filter(
            text(query)).all()  # self.query(session, query, [column for column, value in column_value.items()])
        for dp in DataPackages:
            for column, value in column_value.items():
                setattr(dp, column, value)
        session.commit()


class ActiveFederationsController(TableController):
    def __init__(self):
        self.table = ActiveFederations


class FederationsController(TableController):
    def __init__(self):
        self.table = Federations


class UserTableController(TableController):
    def __init__(self):
        self.table = User
