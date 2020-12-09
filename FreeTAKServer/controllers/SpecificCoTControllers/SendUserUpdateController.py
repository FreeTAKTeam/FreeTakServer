from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.model.SpecificCoT.SendUserUpdate import SendUserUpdate

class SendUserUpdateController(SendCoTAbstractController):
    def __init__(self, RawCoT):
        try:
            tempObject = super().Event.UserUpdate()
            object = SendUserUpdate()
            self.fill_object(object, tempObject, RawCoT)
        except Exception as e:
            print('send user update exception ' + str(e))
