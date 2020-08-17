from .Dest import Dest as DestObject
from lxml import etree

#TODO: modify to call dest with static method
set_count = 0
index_count = 0

class Marti:

    def __init__(self):
        self.dest = [DestObject()]

    @staticmethod
    def other():
        marti = Marti()
        return marti

    @staticmethod
    def geochat():
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
        dest = self.dest[index_count]
        index_count += 1
        return dest
    
    def setdest(self, Dest = None):
        global set_count
        self.dest[set_count] = Dest
        set_count += 1
        self.dest.append(DestObject())

if __name__ == "__main__":
    a = Marti.drop_point()
    print(a.__dict__)
    M = DestObject()
    M.setcallsign('13243432w')
    a.setdest(M)
    for x in a.dest:
        f = a.getdest()
    print('done')