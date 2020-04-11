root = et.Element('event')
xmlheader = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"

def serializerRoot(root, object):
    for key, value in vars(object).items():
        print(str(key)+' '+str(value)+' '+str(hasattr(value, '__dict__')))
        if hasattr(value, '__dict__') == True and isinstance(value, type) == False:
            serializerSub(root, key, value)
        else:
            root.set(key, str(value))
    return xmlheader + et.tostring(root).decode()

def serializerSub(parent, tag, object):
    tag = et.SubElement(parent, tag)
    for key, value in vars(object).items():
        print(str(key)+' '+str(value)+' '+str(hasattr(value, '__dict__')))
        if hasattr(value, '__dict__') == True and isinstance(value, type) == False:
            serializer2(tag, key, value)
        else:
            tag.set(key, str(value))

print(serializerRoot(root, aEvent))