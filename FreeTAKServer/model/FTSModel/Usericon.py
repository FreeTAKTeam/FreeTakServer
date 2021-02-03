from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
#######################################################
#
# usericon.py
# Python implementation of the Class usericon
# Generated by Enterprise Architect
# Created on(FTSProtocolObject):      11-Feb-2020 11(FTSProtocolObject):08(FTSProtocolObject):08 AM
# Original author: Corvo
#
#######################################################
from FreeTAKServer.model.FTSModelVariables.UsericonVariables import UsericonVariables as vars


class Usericon(FTSProtocolObject):
    def __init__(self):
        self.iconsetpath = None

    @staticmethod
    def drop_point(iconsetpath=vars.drop_point().ICONSETPATH):
        usericon = Usericon()
        usericon.seticonsetpath(iconsetpath=iconsetpath)
        return usericon

     # iconsetpath getter
    def geticonsetpath(self):
        return self.iconsetpath

     # iconsetpath setter
    def seticonsetpath(self, iconsetpath=0):
        self.iconsetpath = iconsetpath
