import xml.etree.ElementTree as et

tree = et.ElementTree(et.fromstring('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<event version="2.0" uid="GeoChat.ANDROID-359975090666199.All Chat Rooms.dc77e874-5f5d-4577-ab22-126d40259f14" type="b-t-f" time="2020-04-10T15:41:19.586Z" start="2020-04-10T15:41:19.586Z" stale="2020-04-11T15:41:19.586Z" how="h-g-i-g-o"><point lat="43.855706" lon="-66.108093" hae="14.195624555511682" ce="9.6" le="9999999.0"/><detail><__chat parent="RootContactGroup" groupOwner="false" chatroom="All Chat Rooms" id="All Chat Rooms" senderCallsign="SOLID"><chatgrp uid0="ANDROID-359975090666199" uid1="All Chat Rooms" id="All Chat Rooms"/></__chat><link uid="ANDROID-359975090666199" type="a-f-G-U-C" relation="p-p"/><remarks source="BAO.F.ATAK.ANDROID-359975090666199" to="All Chat Rooms" time="2020-04-10T15:41:19.586Z">hi</remarks><__serverdestination destinations="25.100.242.250:4242:tcp:ANDROID-359975090666199"/></detail></event>'))
attributes = {}
def parseXML(xml):
    for child in xml.iter():
        attributes[child.tag] = child.attrib
parseXML(tree)

finalDict = {}
def createAtribDict(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict) == True:
            createAtribDict(value)
        else:
            finalDict[key] = value

createAtribDict(attributes)
print(finalDict)