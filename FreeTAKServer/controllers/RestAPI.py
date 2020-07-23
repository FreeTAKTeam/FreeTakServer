from flask import Flask, render_template, request
from lxml import etree
from FreeTAKServer.controllers.model.Event import Event
from FreeTAKServer.controllers.model.RawCoT import RawCoT
import datetime as dt
import json

app = Flask(__name__)
APIPipe = None
APIPipe1 = '123'
@app.route("/")
def hello():
    return "Hello World"

@app.route("/Create", methods=['GET'])
def CreateGET():
    return render_template('homeJson.html')

@app.route("/Create", methods=['POST'])
def CreatePOST():
    try:
        COTOutline = b'<event><point/><detail><status/><archive/><usericon/><link/><color/><precisionlocation/><contact/><remarks/></detail></event>'
        data = request.form
        print(data)
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"
        timer = dt.datetime
        now = timer.utcnow()
        zulu = now.strftime(DATETIME_FMT)
        stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + dt.timedelta(minutes=1)
        stale_part = stale_part.strftime(DATETIME_FMT)
        if data.get('Block_Type') == 'Red_Square':
            letter = 'h'
        xmlStructure = '<event version="2.0" uid="{}" type="a-{}-G" time="{}" start="{}" stale="{}" how="h-g-i-g-o">' \
                       '<point lat="{}" lon="{}" hae="9999999.0" ce="9999999.0" le="9999999.0"/>' \
                       '<detail><status readiness="true"/><archive/><usericon iconsetpath="COT_MAPPING_2525B/a-{}/a-{}-G"/>' \
                       '<link uid="{}" production_time="{}" type="a-f-G-U-C" parent_callsign="{}" relation="p-p"/><color argb="-1"/>' \
                       '<archive/><precisionlocation altsrc="???"/>' \
                       '<contact callsign="{}"/>' \
                       '<remarks/>' \
                       '</detail>' \
                       '</event>'.format(data.get('Block_UID'), letter, zulu, zulu, stale_part, data.get('latitude'), data.get('longitude'), letter, letter,
                                         data.get('User_UID'), zulu, data.get('User_Callsign'), data.get('Block_Callsign'))
        submitData(xmlStructure)
        return 'completed', 200
    except Exception as e:
         print(e)

@app.route("/Json", methods=['POST'])
def JsonPost():
    outline = '<event>' \
              '<point/>' \
              '<detail><status/><usericon/>' \
              '<link/>' \
              '<archive/><color/><precisionlocation/>' \
              '<contact/>' \
              '<remarks/>' \
              '</detail>' \
              '</event>'
    event = request.json
    modelObject = Event.dropPoint((etree.fromstring(outline)))
    EventObject = json.loads(event)
    return 'completed', 200

@app.route("/URL", methods=['GET'])
def URLGET():
    data = request.args
    print(data)
    return 'completed', 200

@app.route("/Rest", methods=['GET'])
def RestGET():
    return 'no soup for you', 404

@app.route("/Rest", methods=['POST'])
def RestPOST():
    return 'completed', 200

def submitData(dataRaw):
    global APIPipe
    print(APIPipe)
    data = RawCoT()
    data.clientInformation = "SERVER"
    data.xmlString = dataRaw.encode()
    APIPipe.send([data])

def test(json):
    outline = '<event>' \
              '<point/>' \
              '<detail><status/><usericon/>' \
              '<link/>' \
              '<archive/><color/><precisionlocation/>' \
              '<contact/>' \
              '<remarks/>' \
              '</detail>' \
              '</event>'
    modelObject = Event.dropPoint((etree.fromstring(outline)))
    EventObject = json
    RestAPI().serializeJsonToModel(modelObject, EventObject)

class RestAPI:
    def __init__(self):
        pass

    def startup(self, APIPipea):
        global APIPipe
        APIPipe = APIPipea
        app.run(host="127.0.0.1", port=80)

    def serializeJsonToModel(self, model, Json):
        for key, value in Json.items():
            if isinstance(value, dict):
                submodel = getattr(model, key)
                out = self.serializeJsonToModel(submodel, value)
                setattr(model, key, out)
            else:
                setattr(model, key, value)

if __name__ == '__main__':
    #app.run(host="127.0.0.1", port=80)
    test({'version': '2.0', 'uid': 'dawwa', 'type': 'a-h-G', 'how': 'h-g-i-g-o', 'Point': {'lat': '0', 'lon': '0', 'hae': '9999999.0', 'ce': '9999999.0', 'le': '9999999.0'}, 'detail': {'status': {'readiness': 'true'}, 'usericon': {'iconsetpath': 'COT_MAPPING_2525B/a-h/a-h-G'}, 'Link': {'uid': 'ddwda', 'production_time': '2020-07-23T02:28:32.147Z', 'type': 'a-f-G-U-C', 'parent_callsign': 'dadwadw', 'relation': 'p-p'}, 'color': {'argb': '-1'}, 'precisionlocation': {'m_event.m_detail.m_Precisionlocation.altsrc': '???'}, 'contact': {'m_event.m_detail.m_Contact.callsign': 'avc'}, 'li_6': {'Block_Type': 'h'}}})

