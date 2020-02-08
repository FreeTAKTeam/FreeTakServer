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
        cot_xml =''' 
<?xml version="1.0" standalone="yes"?>
<event
version="2.0"
uid="J-01334"
type="a-.-G-E-W-O"
time="{0}"
start="{0}"
stale="{1}"
how="m-i">
	<detail></detail>
	<point
		lat="30.0090027"
		lon="-85.9578735"
		hae="-42.6"
		ce="45.3"
		le="99.5"/>
</event>
'''.format(zulu, stale)
        f = open("/home/natha/TAK/xmlfile.xml", "a")
        f.write(cot_xml)
        f.close()