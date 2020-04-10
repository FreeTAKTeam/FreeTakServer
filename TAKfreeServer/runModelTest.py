from Controllers.RequestCOTController import RequestCOTController

#below enter the comm type and necesary parameters in arguments
aEvent = RequestCOTController().ping(lat = 123, lon = 123)

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