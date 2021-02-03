from typing import NewType
from FreeTAKServer.model.SpecificCoT.SpecificCoTAbstract import SpecificCoTAbstract
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject


class Types:
    specific_cot = NewType('specific_cot', SpecificCoTAbstract)
    fts_object = NewType('fts_object', FTSProtocolObject)
    test = NewType('test', int)
