import pytest
import xml.etree.ElementTree as ET
from tests.fixtures.classes.pytak_client import PytakClient

class TestDropPointComponent:

    @pytest.mark.asyncio
    async def test_drop_point_marker_2525(self, marker_2525_cot):
        client = PytakClient()
        result = await client.create_and_send_message(marker_2525_cot)
        assert len(result) == 1
        assert ''.join(result[0].decode().split()) == ''.join(ET.tostring(marker_2525_cot).decode().split())