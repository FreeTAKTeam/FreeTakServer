class _Video:

    def __init__(self):
        self.sensor = None
        self.spi = None
        self.url = None

    @classmethod
    def DroneSensor(cls):
        cls.sensor = None
        cls.spi = None
        cls.url = None

        return cls