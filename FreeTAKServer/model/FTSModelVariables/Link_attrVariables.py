class Link_attrVariables:
    def __init__(self):
        self.color = None
        self.type = None
        self.method = None
        self.direction = None
        self.routetype = None
        self.order = None
    
    @classmethod
    def Route(cls):
        cls.COLOR = "-1"
        cls.TYPE = "b-m-r"
        cls.METHOD = "Driving"
        cls.DIRECTION = "Infil"
        cls.ROUTETYPE = "Primary"
        cls.ORDER = "Ascending Check Points"
        return cls