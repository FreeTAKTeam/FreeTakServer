

class createXML:
    def __init__(self):
        #xmllist can be created by adding every initial data to list
        self.xml_list=[b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<event version="2.0" uid="ANDROID-351811095448994" type="a-f-G-U-C" time="2020-02-09T13:20:43.051Z" start="2020-02-09T13:20:43.051Z" stale="2020-02-09T13:26:58.051Z" how="h-e"><point lat="43.967473" lon="-66.126041" hae="41.86958281560347" ce="242.2" le="9999999.0"/><detail><takv os="28" version="3.12.0-45691.45691-CIV" device="SAMSUNG SM-G950W" platform="ATAK-CIV"/><contact endpoint="*:-1:stcp" phone="+19027480992" callsign="C0rv0"/><uid Droid="C0rv0"/><precisionlocation altsrc="GPS" geopointsrc="GPS"/><__group role="Team Member" name="Yellow"/><status battery="92"/><track course="278.424048280084" speed="0.0"/></detail></event>', b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<event version="2.0" uid="ANDROID-7C:91:22:E8:6E:4D" type="a-f-G-U-C" time="2020-02-09T13:21:26.437Z" start="2020-02-09T13:21:26.437Z" stale="2020-02-09T13:27:41.437Z" how="m-g"><point lat="43.855701" lon="-66.108093" hae="14.495629236665277" ce="9.0" le="9999999.0"/><detail><takv device="SAMSUNG SM-G530W" platform="ATAK-CIV" os="22" version="3.12.0-45691.45691-CIV"/><contact phone="19027743142" endpoint="*:-1:stcp" callsign="ghosty"/><uid Droid="ghosty"/><precisionlocation geopointsrc="GPS" altsrc="GPS"/><__group name="Cyan" role="Sniper"/><status battery="89"/><track speed="0.0" course="264.31458179841906"/></detail></event>', b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<event version="2.0" uid="3d587af7-dfb1-475e-bf37-247f27732320" type="a-f-G-U-C-I" time="2020-02-09T19:22:01.2Z" start="2020-02-09T19:22:01.2Z" stale="2020-02-09T19:28:16.2Z" how="h-g-i-g-o"><point lat="0" lon="0" hae="0" ce="9999999" le="9999999"/><detail><takv version="1.10.0.137" platform="WinTAK-CIV" os="Microsoft Windows 10 Home" device="System manufacturer System Product Name"/><contact callsign="NOAH" endpoint="*:-1:stcp"/><uid Droid="NOAH"/><__group name="Cyan" role="Team Member"/><status battery="100"/><track course="0.00000000" speed="0.00000000"/></detail></event>', b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<event version="2.0" uid="ANDROID-351811095448994" type="a-f-G-U-C" time="2020-02-09T13:32:21.428Z" start="2020-02-09T13:32:21.428Z" stale="2020-02-09T13:38:36.428Z" how="h-e"><point lat="43.967473" lon="-66.126041" hae="41.86958281560347" ce="242.2" le="9999999.0"/><detail><takv os="28" version="3.12.0-45691.45691-CIV" device="SAMSUNG SM-G950W" platform="ATAK-CIV"/><contact endpoint="*:-1:stcp" phone="+19027480992" callsign="C0rv0"/><uid Droid="C0rv0"/><precisionlocation altsrc="GPS" geopointsrc="GPS"/><__group role="Team Member" name="Yellow"/><status battery="90"/><track course="247.79986606928483" speed="0.0"/></detail></event>', b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<event version="2.0" uid="ANDROID-351811095448994" type="a-f-G-U-C" time="2020-02-09T13:35:15.473Z" start="2020-02-09T13:35:15.473Z" stale="2020-02-09T13:41:30.473Z" how="h-e"><point lat="43.967473" lon="-66.126041" hae="41.86958281560347" ce="242.2" le="9999999.0"/><detail><takv os="28" version="3.12.0-45691.45691-CIV" device="SAMSUNG SM-G950W" platform="ATAK-CIV"/><contact endpoint="*:-1:stcp" phone="+19027480992" callsign="C0rv0"/><uid Droid="C0rv0"/><precisionlocation altsrc="GPS" geopointsrc="GPS"/><__group role="Team Member" name="Yellow"/><status battery="90"/><track course="248.79580851071282" speed="0.0"/></detail></event>']
        self.xml_string=''
    def xmlparse():
        for xml in xml_list:
            #change xml from byte to ascii
            xml = xml.decode("ascii")
            #remove newline
            xml = xml.split('\n')
            xml = ''.join(xml)
            xml = xml.split('"')
            count = 0
            #find start, time and stale values then replace
            for value in xml:
                if value == ' time=' or value == ' start=':
                    xml[count+1] = "{0}"
                    count += 1
                elif value == ' stale=':
                    xml[count+1] = "{1}"
                    count +=1
                else:
                    count +=1
            #reconnect xmlstring
            xml = '"'.join(xml)
            xml_string = xml_string + xml

    def changeDate():
        #create current datetime format
        timer = dt.datetime
        now = timer.utcnow()
        zulu = now.strftime(DATETIME_FMT)
        stale_part = now.minute + 1
        if stale_part > 59:
            stale_part = stale_part - 60
        stale_now = now.replace(minute=stale_part)
        stale = stale_now.strftime(DATETIME_FMT)
        #apply to xml string
        xml_string = xml_string.format(zulu, stale)
        print(xml_string)
