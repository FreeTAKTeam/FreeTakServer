import pytest
import xml.etree.ElementTree as ET

@pytest.fixture
def marker_2525_cot() -> ET.Element:
    event = ET.Element("event", {
        'version': "2.0",
        'type': "a-u-G",
        'uid': "a0c524c6-0422-4382-9981-e39d1dc71730",
        'how': "m-g",
        'time': "2020-12-16T19:59:34.910Z",
        'start': "2020-12-16T19:59:34.910Z",
        'stale': "2021-01-02T20:40:03.838Z",
    })

    point = ET.Element("point", {
        'lat': "38.856650047254725",
        'lon': "-77.06364199776728",
        'hae': "9999999.0",
        'ce': "9999999.0",
        'le': "9999999.0",
    })

    status = ET.Element("status", {
        'readiness': "true"
    })

    archive = ET.Element("archive")

    link = ET.Element("link", {
        'uid': "ANDROID-589520ccfcd20f01",
        'production_time': "2020-12-16T19:50:57.629Z",
        'type': "a-f-G-U-C",
        'parent_callsign': "HOPE",
        'relation': "p-p",
    })

    contact = ET.Element("contact", {
        'callsign': "U.16.135057"
    })
    
    remarks = ET.Element("remarks")

    color = ET.Element("color", {
        'argb': "-1"
    })

    precision_location = ET.Element("precisionlocation", {
        'altsrc': "???"
    })

    user_icon = ET.Element("usericon", {
        'iconsetpath': "COT_MAPPING_2525B/a-u/a-u-G"
    })

    # Build detail
    detail = ET.Element("detail")
    ET.SubElement(detail, status.tag, status.attrib)
    ET.SubElement(detail, link.tag, link.attrib)
    ET.SubElement(detail, contact.tag, contact.attrib)
    ET.SubElement(detail, remarks.tag, remarks.attrib)
    ET.SubElement(detail, color.tag, color.attrib)
    ET.SubElement(detail, precision_location.tag, precision_location.attrib)
    ET.SubElement(detail, user_icon.tag, user_icon.attrib)

    # Build event
    ET.SubElement(event, point.tag, point.attrib)
    ET.SubElement(event, detail.tag, detail.attrib)

    return event
