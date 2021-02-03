import shutil
from sqlalchemy.sql import text


class TableController:
    # default constructor  def __init__(self):
    def __init__(self):
        self.table = None

    def delete(self, session, query):
        # this function removes a row from the datapackages table based on the uid
        session.query(self.table).filter(text(query)).delete(synchronize_session='fetch')
        session.commit()
        return 1

    def create(self, session, **args):
        # this function adds a new row to the datapackages table
        session.add(self.table(**args))
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
