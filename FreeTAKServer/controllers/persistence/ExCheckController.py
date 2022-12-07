from FreeTAKServer.model.SQLAlchemy.ExCheck import ExCheck
from FreeTAKServer.model.SQLAlchemy.ExCheck import ExCheckData
from FreeTAKServer.model.ExCheck.templateInstanceContents import templateInstanceContents
from FreeTAKServer.controllers.persistence.table_controllers import TableController
from FreeTAKServer.model.SQLAlchemy.ExCheckKeywords import ExCheckKeywords
from sqlalchemy.sql import text
unsuportedAttribs = ['_sa_instance_state']
#TODO: move out all serializers into a serializers controller

class ExCheckController(TableController):

    def __init__(self):
        self.table = ExCheck

    def queryChildren(self, query, columns, session):
        from FreeTAKServer.model.SQLAlchemy.ExCheckData import ExCheckData
        output = session.query(self.table).join(ExCheckData, self.table.data).filter(text(query)).all()
        return output

    def create(self, session, object):
        row = self.convert_exCheck_model_to_row(object)
        session.add(row)
        session.commit()

    def convert_exCheck_model_to_row(self, modelObject):
        if isinstance(modelObject, templateInstanceContents):
            exCheck_row = ExCheck()
            for attribName, attribValue in modelObject.__dict__.items():
                if attribName not in unsuportedAttribs:
                    if attribName == 'data':
                        data_row = ExCheckData()
                        for attribName, attribValue in attribValue.__dict__.items():
                            if attribName not in unsuportedAttribs:
                                if isinstance(attribValue, list):
                                    keyword_row = ExCheckKeywords()
                                    keyword_row.name = attribValue[0]
                                    keyword_row.description = attribValue[1]
                                    keyword_row.callsign = attribValue[2]
                                    setattr(data_row, attribName, keyword_row)

                                else:
                                    setattr(data_row, attribName, attribValue)

                        setattr(exCheck_row, 'data', data_row)
                    else:
                        setattr(exCheck_row, attribName, attribValue)
                else:
                    pass
            return exCheck_row
        else:
            raise TypeError('incorrect object passed to convert_exCheck_model_to_row')