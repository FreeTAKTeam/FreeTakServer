#######################################################
#
# Emergency.py
# Python implementation of the Class Emergency
# Generated by Enterprise Architect
# Created on:      04-Nov-2020 4:26:40 PM
# Original author: natha
#
#######################################################
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations


def requesttype(currenttype, supportedtype):
    def wrapper(func):
        def callfunc(*args, **kwargs):
            if currenttype == supportedtype:
                func(*args, **kwargs)
            else:
                raise AttributeError
        return callfunc
    return wrapper


class Emergency:
    # default constructor  def __init__(self):
    emergencyType = ""
    # the type of emergency to be displayed
    # the name of the person that has an emergency.
    name = ""
    # server generated Unique Id of this emergency
    latitude = ''
    longitude = ''
    uid = ''
    # @requesttype(type, "DELETE")

    def getuid(self):
        return self._uid

    # @requesttype(type, "DELETE")
    def setuid(self, value: str) -> None:
        if self.type == "DELETE":
            self._uid = value
        else:
            raise AttributeError('Emergency has no attribute uid')

    def getemergencyType(self):
        # if self.type == "POST":
        pass

    def setemergencyType(self, emergencyType):
        self.emergencyType = emergencyType

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def setlatitude(self, latitude):
        self.latitude = str(latitude)

    def getlatitude(self):
        if self.latitude == '':
            return '0'
        else:

            return self.latitude

    def setlongitude(self, longitude):
        self.longitude = str(longitude)

    def getlongitude(self):
        if self.longitude == '':
            return '0'
        else:
            return self.longitude


if __name__ == "__main__":
    Emergency("DELETE").uid = '123'
