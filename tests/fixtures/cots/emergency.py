import pytest
import xml.etree.ElementTree as ET

@pytest.fixture
def emergency_cot() -> ET.Element:
    event = ET.Element("event", {
        'version': "2.0",
        'type': "b-a-o-tbl",
        'uid': "7e674c38-a156-4ae0-93a9-f906e95ec665",
        'how': "h-e",
        'time': "2022-12-16T19:59:34.910Z",
        'start': "2022-12-16T19:59:34.910Z",
        'stale': "2024-01-02T20:40:03.838Z",
    })

    point = ET.Element("point", {
        'lat': "38.856650047254725",
        'lon': "-77.06364199776728",
        'hae': "9999999.0",
        'ce': "9999999.0",
        'le': "9999999.0",
    })

    link = ET.Element("link", {
        'uid': "ANDROID-589520ccfcd20f01",
        'production_time': "2022-12-16T19:50:57.629Z",
        'type': "a-f-G-U-C-I",
        'relation': "p-p",
    })

    contact = ET.Element("contact", {
        'callsign': "U.16.135057"
    })

    # Build detail
    detail = ET.Element("detail")
    ET.SubElement(detail, link.tag, link.attrib)
    ET.SubElement(detail, contact.tag, contact.attrib)

    # Build event
    ET.SubElement(event, point.tag, point.attrib)
    ET.SubElement(event, detail.tag, detail.attrib)

    return event
