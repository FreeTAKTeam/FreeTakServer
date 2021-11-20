import uuid
import random


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


class TestAPIData:
    postKMLAddress = {
        "name": "have fun with Kovid1984!!!",
        "address": "New York",
        "body":
            {
                "userCallsign": "Savage",
                "dateTime": "2021-10-23",
                "type": "Surveillance",
                "eventScale": "global",
                "importance": "Crucial",
                "status": "FurtherInvestigation",
                "Time Observed": "2021-10-13T13:55:05.19Z",
                "Duration of Event": "All day",
                "Method Of Detection": "General Observation",
                "Surveillance Type": "Discreet",
                "Assessed Threats": "Democracy",
                "Final Remarks": "SNAFU"
            }
    }

    postVideo_streams = {
        "streamAddress": "http://138.197.129.27",
        "streamPort": "1935",
        "streamPath": "/LiveApp/342508189321134315564775",
        "alias": "Demo Stream From API",
        "streamProtocol": "rtsp"
    }

    @property
    def postGeoObject(self):
        return [
            {
                "longitude": random.randint(-180, 80),
                "geoObject": "Rifleman",
                "latitude": random.randint(-90, 90),
                "attitude": "unknown",
                "how": "nonCoT",
                "name": "target",
                "Bearing": 0.8000,
                "timeout": 6000
            },
            {
                "geoObject": "Rifleman",
                "address": "1600 Pennsylvania Avenue NW, Washington, DC 20500, USA",
                "attitude": "unknown",
                "how": "nonCoT",
                "name": "target",
                "Bearing": 0.8000,
                "timeout": 6000
            }]

    @property
    def putGeoObject(self):
        return {"uid": "changeme",
                "longitude": random.randint(-180, 80),
                "geoObject": "Rifleman",
                "latitude": random.randint(-90, 90),
                "attitude": "friendly",
                "how": "nonCoT",
                "name": "target",
                "Bearing": 0.8000,
                "timeout": 6000
                }

    @property
    def postPresence(self):
        return {
            "how": "nonCoT",
            "name": "testing",
            "latitude": str(random.randint(-180, 80)),
            "longitude": str(random.randint(-180, 80)),
            "role": "Team Member",
            "team": "Cyan"
        }

    @property
    def putPresence(self):
        return {
            "uid": "change-me",
            "how": "nonCoT",
            "name": "testing",
            "latitude": str(random.randint(-180, 80)),
            "longitude": str(random.randint(-180, 80)),
            "role": "Team Member",
            "team": "Cyan"
        }