from .SpecificCoTAbstract import SpecificCoTAbstract

class SendSensorDrone(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("SensorDrone")