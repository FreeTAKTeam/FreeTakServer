from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.model.SpecificCoT.SendTakPong import SendTakPong


class SendTakPongController(SendCoTAbstractController):
    def __init__(self, RawCoT):
        tempObject = super().Event.takPong()
        object = SendTakPong()
        self.fill_object(object, tempObject, RawCoT)
