from Controllers.RequestCOTController import RequestCOTController

#below enter the comm type and necesary parameters in arguments
aEvent = RequestCOTController().chat(chatType = 'chatToAll', senderCallsign = 'a', chatroom = 'b', groupOwner = 'c', id = 'd', parent = 'e', chatgrpuid0 = 'f', chatgrpuid1 = 'g', chatgrpid = 'h')
print('over')
#dont worry about it below here
'''
attrDict = {}
def search(y):
    attrDict[y.__class__.__name__] = vars(y)
    for x, v in vars(y).items():
        print(str(x)+' '+str(v)+' '+str(hasattr(v, '__dict__')))
        if hasattr(v, '__dict__') == True and isinstance(v, type) == False:
            search(v)
search(aEvent)
print(attrDict)
print('over')
'''