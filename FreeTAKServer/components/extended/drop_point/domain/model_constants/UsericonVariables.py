class UsericonVariables:
    def __init__(self):
        self.ICONSETPATH = "DEFAULT"

    @classmethod
    def drop_point(cls):
        cls.ICONSETPATH = "DEFAULT"
        return cls