from FreeTAKServer.model.FTSModel.Dest import Dest as DestObject

#TODO: modify to call dest with static method
set_count = 0
index_count = -1

class Marti:

    def __init__(self):
        self.dest = [DestObject()]

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
        global index_count
        index_counta = index_count
        dest = self.dest[index_count]
        index_count += 1
        return dest
    
    def setdest(self, Dest = None):
        global set_count
        self.dest[set_count] = Dest
        set_count += 1
        self.dest.append(DestObject())

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