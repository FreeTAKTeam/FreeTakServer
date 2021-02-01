from FreeTAKServer.model.protobufModel import fig_pb2
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.model.SpecificCoT.SendFederatedCoT import SendFederatedCoT
from FreeTAKServer.model.FTSModel.Event import Event
from lxml import etree
import datetime

class FederatedCoTController:
    def __init__(self):
        pass

    def serialize_from_FTS_model(self):
        pass

    def serialize_main_contentv1(self, protoobject, ftsobject):
        print('beginning serialization to FT')
        try:
            event = protoobject.event


            # the following try and except statements format milliseconds to CoT compatible DT
            try:
                datetime.datetime.strftime(datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(float(event.sendTime) / 1000.0)), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%dT %H:%M:%S.%fZ")
            except:
                datetime.datetime.strftime(datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(float(event.sendTime) / 1000.0)), "%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%dT %H:%M:%S.%fZ")

            try:
                formatedDatatime = str(datetime.datetime.fromtimestamp(float(event.startTime) / 1000.0))
                datetime.datetime.strftime(datetime.datetime.strptime(formatedDatatime, "%Y-%m-%d %H:%M:%S"), "%Y-%m-%dT %H:%M:%S.%fZ")
            except Exception as e:
                formatedDatatime = str(datetime.datetime.fromtimestamp(float(event.startTime) / 1000.0))
                datetime.datetime.strftime(datetime.datetime.strptime(formatedDatatime, "%Y-%m-%d %H:%M:%S.%f"),"%Y-%m-%dT %H:%M:%S.%fZ")

            try:
                datetime.datetime.strftime(datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(float(event.staleTime) / 1000.0)), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%dT %H:%M:%S.%fZ")
            except:
                datetime.datetime.strftime(datetime.datetime.strptime(str(datetime.datetime.fromtimestamp(float(event.staleTime) / 1000.0)), "%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%dT %H:%M:%S.%fZ")

            ftsobject.setuid(event.uid)
            ftsobject.settype(event.type)
            ftsobject.sethow(event.coordSource)

            point = ftsobject.getpoint()
            point.setce(event.ce)
            point.setle(event.le)
            point.setlon(event.lon)
            point.setlat(event.lat)
            point.sethae(event.hae)

            ftsobject.setpoint(point)

            detail = event.other

            obj = SendFederatedCoT()
            obj.modelObject = ftsobject
            tempxmlstring = etree.fromstring(XMLCoTController().serialize_model_to_CoT(ftsobject))
            eventString = tempxmlstring
            eventString.append(etree.fromstring(detail.encode()))
            obj.xmlString = etree.tostring(eventString)
            print('serialized protobuf to ' + str(obj.xmlString))
            return obj
        except Exception as e:
            print(e)
            return -1
    def serialize_from_FTS_modelv1(self, federatedevent, ftsobject):
        try:
            xml = ftsobject.xmlString
            detail = etree.fromstring(xml)
            detail = detail.find('detail')
            model = ftsobject.modelObject
            event = federatedevent.event
            """contact = federatedevent.contact
            contact.operation = 1
            contact.uid = '1293454'
            contact.callsign = 'TEST'
            contact.phone = '190233333333'
            contact.sip = '13245r43'
            contact.directConnect = '3ddwdawwd'"""
            try:
                event.sendTime = int(model.gettime())
            except:
                event.sendTime = int(datetime.datetime.strptime(model.gettime(), "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000)
            try:
                event.startTime = int(model.getstart())
            except:
                event.startTime = int(datetime.datetime.strptime(model.getstart(), "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000)
            try:
                event.staleTime = int(model.getstale())
            except:
                event.staleTime = int(datetime.datetime.strptime(model.getstale(), "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000)
            event.uid = model.getuid()
            event.type = model.gettype()
            event.coordSource = model.gethow()
            event.other = etree.tostring(detail)

            point = model.getpoint()
            event.lat = float(point.getlat())
            event.lon = float(point.getlon())
            event.hae = float(point.gethae())
            event.ce = float(point.getce())
            event.le = float(point.getle())

            return federatedevent
        except Exception as e:
            print('exception in serialize from FTS')
            print(e)
            return -1
    def serialize_to_FTS_modelv1(self,protoobject ,ftsobject):
        pass

    def serialize_to_FTS_modelv2(self, protoobject, ftsobject):

        for field in protoobject.DESCRIPTOR.fields:
            if field.message_type != None:
                #get the getter associated with the field
                FTSgetter = getattr(ftsobject, 'get' + field.name)

                #get the content of the associate FTSobject nested attribute
                newftsobject = FTSgetter()

                #get the protobuf objects nested message
                protoObjectValue = getattr(protoobject, field.name)

                #call serializer with both nested value from protoObject and newftsobject
                nestedObject = self.serialize_to_FTS_model(protoObjectValue, newftsobject)

                #get setter for associated fts object attribute
                ftssetter = getattr(ftsobject, 'set' + field.name)

                # call the fts setter
                ftssetter(nestedObject)

            else:
                #get setter for associated fts object attribute
                FTSSetter = getattr(ftsobject, 'set'+field.name)

                # get the protobuf objects nested message
                protoObjectValue = getattr(protoobject, field.name)

                # call the fts setter with the object value
                FTSSetter(protoObjectValue)

        return ftsobject

if __name__ == "__main__":
    ftsobj = Event.FederatedCoT()

    msga = fig_pb2.FederatedEvent()
    geo = msga.event
    geo.sendTime = 1
    geo.startTime = 2
    geo.staleTime = 3
    geo.lat = 4
    geo.lon = 5
    geo.hae = 6
    geo.ce = 7
    geo.le = 8
    geo.uid = '9'
    geo.type = '10'
    geo.coordSource = '11'
    geo.other = '<detail/>'

    new = FederatedCoTController().serialize_main_contentv1(msga, ftsobj)
    ol = FederatedCoTController().serialize_from_FTS_modelv1(fig_pb2.FederatedEvent(), new)

