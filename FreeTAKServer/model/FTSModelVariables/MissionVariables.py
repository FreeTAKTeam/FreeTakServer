class MissionVariables:

    @classmethod
    def ExcheckUpdate(cls):
        cls.TYPE = 'CHANGE'
        cls.TOOL = "ExCheck"
        cls.NAME = None
        cls.AUTHORUID = None
        return cls
