from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.Dest import Dest as DestObject

# TODO: modify to call dest with static method


class counter:
    count = 0
    getter_called = False


class Marti(FTSProtocolObject):
    __counter = counter()

    def __init__(self):
        # self.__dest = [DestObject(self.__counter)]
        # self.__tempdest = self.__dest
        self.dest = [DestObject(self.__counter)]
        self.__index = 0
        self.__firstrun = True

    @staticmethod
    def other():
        global set_count, index_count
        set_count = 0
        index_count = 0
        marti = Marti()
        return marti

    @staticmethod
    def geochat():
        global set_count, index_count
        set_count = 0
        index_count = 0
        marti = Marti()
        return marti

    @staticmethod
    def drop_point():
        global set_count, index_count
        set_count = 0
        index_count = 0
        marti = Marti()
        return marti

    def getdest(self):
        # TODO: clean up this implementation and eliminate need for __firstrun
        try:
            returnvalue = self.dest[self.__index]
            if returnvalue._gettercalled() is False and returnvalue._settercalled() is False and self.__index == 0:
                # only when no changes have been made
                return returnvalue
            elif returnvalue._gettercalled() and returnvalue._settercalled() is False and self.__index != 0:
                returnvalue = self.dest[self.__index]
                self.__index += 1
                return returnvalue
            elif returnvalue._gettercalled() and returnvalue._settercalled():
                self.__index += 1
                returnvalue = self.dest[self.__index]
                return returnvalue
            elif returnvalue._settercalled() and returnvalue._gettercalled() is False and returnvalue.callsign is not None and self.__firstrun:
                # value has already been set and therefore new instance of dest must be returned
                self.setdest()
                returnvalue = self.dest[self.__index]
                return returnvalue
            elif not returnvalue._settercalled() and not returnvalue._gettercalled() and returnvalue.callsign is None and self.__index == 0:
                return returnvalue
            elif not returnvalue._settercalled() and not returnvalue._gettercalled() and returnvalue.callsign is None:
                self.__index = 0
                self.__firstrun = False
                returnvalue = self.dest[self.__index]
                return returnvalue
            return returnvalue
        except IndexError:
            try:
                if self.__firstrun:
                    self.setdest()
                    returnvalue = self.dest[self.__index]
                    return returnvalue
                else:
                    self.__index = 0
                    return self.dest[self.__index]
            except IndexError:
                self.__index = 0
                return self.dest[self.__index]

    def setdest(self, Dest=None):
        if not Dest:
            Dest = DestObject(self.__index)
        self.dest.append(Dest)
        self.__index += 1


if __name__ == "__main__":
    from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
    from lxml import etree
    a = Marti.other()
    b = etree.fromstring(b'<marti><dest callsign = "bbbb"/></marti>')
    x = XMLCoTController().serialize_CoT_to_model(a, b)
    y = x.getdest().callsign
    print(a.__dict__)
    M = DestObject()
    M.setcallsign('13243432w')
    a.setdest(M)
    for x in a.dest:
        f = a.getdest()
    print('done')
