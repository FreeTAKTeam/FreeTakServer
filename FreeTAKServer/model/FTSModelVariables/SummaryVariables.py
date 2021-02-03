class SummaryVariables:
    def __init__(self):
        self.INTAG = None

    @classmethod
    def drop_point(cls):
        # appears to be present on points shared over gottena
        cls.INTAG = None
        return cls
