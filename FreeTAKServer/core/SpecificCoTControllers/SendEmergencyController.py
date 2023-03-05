from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
from FreeTAKServer.core.SpecificCoTControllers.SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.model.SpecificCoT.SendEmergency import SendEmergency


class SendEmergencyController(SendCoTAbstractController):
    def __init__(self, RawCoT):
        if RawCoT.status == 'on':
            tempObject = super().Event.emergecyOn()
            object = SendEmergency()
            object.status = 'on'
            self.fill_object(object, tempObject, RawCoT, addToDB=False)
            obj = self.getObject()
            DatabaseController().create_ActiveEmergency(obj.modelObject)

        elif RawCoT.status == 'off':
            tempObject = super().Event.emergecyOff()
            object = SendEmergency()
            object.status = 'off'
            self.fill_object(object, tempObject, RawCoT, addToDB=False)
            obj = self.getObject()
            DatabaseController().remove_ActiveEmergency(query=f'uid = "{obj.modelObject.uid}"')
