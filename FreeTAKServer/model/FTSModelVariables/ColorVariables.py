class ColorVariables:
    def __init__(self):
        ARGB = None

    @classmethod
    def drop_point(cls):
        cls.ARGB = "-1"
        return cls