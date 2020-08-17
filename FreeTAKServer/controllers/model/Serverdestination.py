#######################################################
# 
# __serverdestination.py
# Python implementation of the Class __serverdestination
# Generated by Enterprise Architect
# Created on:      11-Feb-2020 11:08:10 AM
# Original author: Corvo
# 
#######################################################
from .ServerdestinationVariables import ServerdestionationVariables as vars

class _Serverdestination:
    def __init__(self):
        # string composed by IP:port: protocol:machineID. e.g. 192.168.0.103:4242:tcp:
        # ANDROID-R52JB0CDC4E
        self.destinations = None
        # destinations getter

    @staticmethod
    def geochat(DESTINATIONS = vars.geochat().DESTINATIONS):
        serverdestinations = _Serverdestination()
        serverdestinations.setdestinations(DESTINATIONS)
        return serverdestinations

    def getdestinations(self): 
        return self.destinations 

    # destinations setter 
    def setdestinations(self, destinations=None):
        self.destinations = destinations
