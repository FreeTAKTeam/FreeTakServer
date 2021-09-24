import uuid

class TestCoTClient:
    ''' this class generates the cot for a basic client
    '''
    def __init__(self, callsign: str = str(uuid.uuid4()), uid: str = str(uuid.uuid4())):
        self.callsign = callsign
        self.uid = uid

    def generate_cot(self):
        return f'<event version="2.0" uid="{self.uid}" type="a-f-G-U-C-I" time="2021-09-19T23:47:48.79Z" start="2021-09-19T23:47:48.79Z" stale="2021-09-21T23:49:03.79Z" how="h-g-i-g-o"> <point lat="0" lon="0" hae="0" ce="9999999" le="9999999" /> <detail> <contact callsign="{self.callsign}"/> <__group name="Yellow" role="Team Member" /></detail> </event>'.encode()