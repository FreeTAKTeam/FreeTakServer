from Controllers.RequestCOTController import RequestCOTController
import xml.etree.ElementTree as et

#below enter the comm type and necesary parameters in arguments
#aEvent = RequestCOTController().chat(chatType = 'chatToAll', senderCallsign = 'a', chatroom = 'b', groupOwner = 'c', id = 'd', parent = 'e', uid0 = 'f', uid1 = 'g', chatgrpid = 'd')
aEvent  = RequestCOTController().ping(lat = 123, lon = 456, hae = 789)
print('over')

