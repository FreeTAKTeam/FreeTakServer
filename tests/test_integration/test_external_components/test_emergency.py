import pytest
import xml.etree.ElementTree as ET

from tests.fixtures.classes.pytak_client import PytakClient
from tests.fixtures.cots.emergency import emergency_cot

class TestEmergencyComponent:

    @pytest.mark.asyncio
    async def test_emergency(self, emergency_cot):
        client = PytakClient()
        result = await client.create_and_send_message(emergency_cot)
        assert len(result) == 1
        assert ''.join(result[0].decode().split()) == ''.join(ET.tostring(emergency_cot).decode().split())