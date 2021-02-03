from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.model.SpecificCoT.SendUserUpdate import SendUserUpdate


class SendUserUpdateController(SendCoTAbstractController):
    def __init__(self, RawCoT=None):
        try:
            tempObject = super().Event.UserUpdate()
            object = SendUserUpdate()
            if RawCoT is not None:
                self.fill_object(object, tempObject, RawCoT)
            else:
                pass
        except Exception as e:
            print('send user update exception ' + str(e))
