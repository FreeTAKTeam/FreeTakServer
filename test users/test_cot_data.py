import uuid

class TestCoTClient:
    ''' this class generates the cot for a basic client
    '''
    def __init__(self, callsign: str = None, uid: str = None):
        if not callsign:
            callsign = str(uuid.uuid4())
        if not uid:
            uid = str(uuid.uuid4())
        self.callsign = callsign
        self.uid = uid

    def generate_object_cot(self):
        return f'<event version="2.0" uid="{self.uid}" type="a-f-G" how="h-g-i-g-o" time="2021-04-02T14:53:32Z" start="2021-04-02T14:53:32Z" stale="2022-04-02T14:53:32Z"> <point lat="0" lon="0" hae="603.04" le="9999999" ce="9999999" /> <detail> <contact callsign="{self.callsign}" /> <link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" relation="p-p" production_time="2021-04-02T14:53:32Z" /> <archive /> <usericon iconsetpath="COT_MAPPING_2525B/a-f/a-f-G" /> <precisionlocation altsrc="DTED0" /> </detail> </event>'.encode()

    def generate_cot(self):
        return f'<event version="2.0" uid="{self.uid}" type="a-f-G-U-C-I" time="2021-09-19T23:47:48.79Z" start="2021-09-19T23:47:48.79Z" stale="2021-09-21T23:49:03.79Z" how="h-g-i-g-o"> <point lat="0" lon="0" hae="0" ce="9999999" le="9999999" /> <detail> <contact callsign="{self.callsign}"/> <__group name="Yellow" role="Team Member" /></detail> </event>'.encode()