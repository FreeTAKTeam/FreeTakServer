import datetime as dt
import uuid
import xml.etree.ElementTree as ET
import socket
import logging

logger = logging.getLogger("django")

ID = {
    "pending": "p",
    "unknown": "u",
    "assumed-friend": "a",
    "friend": "f",
    "neutral": "n",
    "suspect": "s",
    "hostile": "h",
    "joker": "j",
    "faker": "f",
    "none": "o",
    "other": "x"
}
DIM = {
    "space": "P",
    "air": "A",
    "land-unit": "G",
    "land-equipment": "G",
    "land-installation": "G",
    "sea-surface": "S",
    "sea-subsurface": "U",
    "subsurface": "U",
    "other": "X"
}

DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"

class CursorOnTarget:

    def atoms():
        timer = dt.datetime
        now = timer.utcnow()
        zulu = now.strftime(DATETIME_FMT)
        stale_part = now.minute + 1
        if stale_part > 59:
            stale_part = stale_part - 60
        stale_now = now.replace(minute=stale_part)
        stale = stale_now.strftime(DATETIME_FMT)
        cot_xml = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><event version='2.0' uid='deccf9b1-ee37-4205-a235-a6d527fc7c24' type='a-f-G' time='{0}' start='{0}' stale='{1}' how='h-g-i-g-o'><point lat='44.2198868' lon='-66.1382602' hae='-13.62' ce='9999999.0' le='9999999.0' /><detail><link uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' production_time='2020-02-01T18:48:14Z' relation='p-p' type='a-f-G' parent_callsign='Eliopoli HQ'/><archive/><usericon iconsetpath='COT_MAPPING_2525B/a-f/a-f-G'/><precisionlocation altsrc='DTED0'/><contact callsign='F.1.184814'/></detail></event>".format(zulu, stale)
        f = open("/home/natha/TAK/xmlfile.xml", "a")
        f.truncate()
        f.write(cot_xml)
        f.close()
        print(cot_xml)
        print('running')
