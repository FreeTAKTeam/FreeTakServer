from .SpecificCoTAbstract import SpecificCoTAbstract


class SendFederatedCoT(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("FederatedCoT")
