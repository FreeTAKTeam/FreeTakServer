from sqlalchemy.inspection import inspect


class SqlAlchemyObjectController:
    def __init__(self):
        pass

    def convert_sqlalchemy_to_modelobject(self, SqlAlchemyObject, modelObject):
        for attribute in SqlAlchemyObject.__dict__.keys():
            if attribute != '_sa_instance_state' and attribute != 'PrimaryKey' and attribute != 'xmlString' and SqlAlchemyObject.__dict__[attribute] is not None:
                try:
                    setter = getattr(modelObject, 'set' + attribute)
                    setter(SqlAlchemyObject.__dict__[attribute])
                except Exception as e:
                    print(str(e))
            else:
                pass

        for relationship in SqlAlchemyObject.__mapper__.relationships:
            try:
                y = str(relationship)
                relationship = '.'.join(str(relationship).split('.', 1)[1::])
                relationshipObject = getattr(SqlAlchemyObject, relationship)
                if relationshipObject is not None:
                    modelObjectInstance = getattr(modelObject, relationship)
                    setter = getattr(modelObject, 'set' + relationship)
                    setter(self.convert_sqlalchemy_to_modelobject(relationshipObject, modelObjectInstance))
                else:
                    pass
            except Exception as e:
                print(str(e))
        return modelObject


if __name__ == "__main__":
    from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController

    contr = DatabaseController().query_ActiveEmergency()
    x = contr[0]
    from FreeTAKServer.model.FTSModel.Event import Event
    modelobj = Event.emergecyOn()

    y = SqlAlchemyObjectController().convert_sqlalchemy_to_modelobject(x.event, modelobj)
    1 == 1
