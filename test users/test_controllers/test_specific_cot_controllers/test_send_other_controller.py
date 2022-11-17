from unittest import TestCase
from FreeTAKServer.controllers.SpecificCoTControllers.SendOtherController import SendOtherController
from FreeTAKServer.model.RawCoT import RawCoT

class Test_SendOtherController(TestCase):

    def test_init(self):
        raw_cot = RawCoT()
        raw_cot.xmlString = '<event version="2.0" uid="testuid" type="xyz" how="h-g-i-g-o" time="2021-01-22T01:13:00Z" start="2021-01-22T01:13:00Z" stale="2022-01-22T01:13:00Z"><point lat="0" lon="0" hae="9999999" le="9999999" ce="9999999" /><detail><contact callsign="F.22.011300" /><nfoif/>ffhhtrerew<ffenis></ffenis><marti><dest callsign="test"/></marti></detail></event>'
        other_cot = SendOtherController(raw_cot)
        assert other_cot.object.modelObject.detail.marti.dest[0].callsign == "test"
