from sqlalchemy.inspection import inspect

class SqlAlchemyObjectController:
    def __init__(self):
        pass

    def convert_sqlalchemy_to_modelobject(self, SqlAlchemyObject, modelObject, source = None):
        """ this serializer converts any sqlalchemy object to it's associate model objects
                the attributes of the sqlalchemy object are first iterated over and then the setter
                associated with this attribute in the model object is called with the sqlalchemy value.

                the relationships are then iterated over, relationships represent nested tags within xml.
                each nested element however also has a relationship to it's parent and so the source argument is
                passed to ignore the parent relationship.
        Args:
            SqlAlchemyObject:
            modelObject:
            source:

        Returns:

        """
        for attribute in SqlAlchemyObject.__dict__.keys():
            if attribute != '_sa_instance_state' and attribute != 'PrimaryKey' and attribute != 'xmlString' and SqlAlchemyObject.__dict__[attribute] != None:
                try:
                    setter = getattr(modelObject, 'set'+attribute)
                    setter(SqlAlchemyObject.__dict__[attribute])
                except Exception as e:
                    print(str(e))
            else:
                pass

        for relationship in SqlAlchemyObject.__mapper__.relationships:
            try:
                relationship = '.'.join(str(relationship).split('.', 1)[1::])
                if relationship != source:
                    relationshipObject = getattr(SqlAlchemyObject, relationship)
                    if relationshipObject != None:
                        modelObjectInstance = getattr(modelObject, relationship)
                        setter = getattr(modelObject, 'set'+relationship)
                        setter(self.convert_sqlalchemy_to_modelobject(relationshipObject, modelObjectInstance, source=type(SqlAlchemyObject).__name__))
                    else:
                        pass
            except Exception as e:
                print(str(e))
        return modelObject

