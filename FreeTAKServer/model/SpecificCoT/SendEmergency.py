from .SpecificCoTAbstract import SpecificCoTAbstract


class SendEmergency(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType('Emergency')
        self.setPlaceInternalArray(True)
        self.setStatus('')

    def setPlaceInternalArray(self, placeInternalArray):
        self.placeInternalArray = placeInternalArray

    def getPlaceInternalArray(self):
        return self.placeInternalArray

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status
