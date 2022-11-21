class AbstractPythonSerializer:
    def __init__(self, object):
        self.pythonobject = object

    def serializeObject(self):
        for item in vars(self.pythonobject):

            if isinstance(getattr(self.pythonobject, item), list):
                self.list(item)
            elif isinstance(getattr(self.pythonobject, item), dict):
                self.dict(item)
            elif (str(type(getattr(self.pythonobject, item))).split("'")[1]).split('.')[0] == 'FreeTAKServer':
                self.object(item)
            else:
                self.other(item)

    def list(self, obj):
        pass

    def dict(self, obj):
        pass

    def object(self, obj):
        pass

    def other(self, obj):
        pass
