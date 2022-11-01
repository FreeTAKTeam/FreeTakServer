import time
import pytest
import multiprocessing
import xml.etree.ElementTree as ET
from tests.fixtures.classes.pytak_client import PytakClient
from tests.fixtures.cots.marker import marker_2525_cot
from FreeTAKServer.controllers.services import FTS as fts
from FreeTAKServer.model.ServiceObjects.FTS import FTS as FTSObj


def server_process():
    return fts.FTS().startup(
        FTSObj().CoTService.CoTServicePort, #COT Port
        FTSObj().CoTService.CoTServiceIP, #COT IP
        FTSObj().TCPDataPackageService.TCPDataPackageServicePort, #DataPackage Port
        FTSObj().TCPDataPackageService.TCPDataPackageServiceIP, #DataPackage IP
        FTSObj().SSLDataPackageService.SSLDataPackageServicePort, #SSLDataPackage Port
        FTSObj().SSLDataPackageService.SSLDataPackageServiceIP, #SSL DataPackage IP
        FTSObj().RestAPIService.RestAPIServicePort, #RestAPI Port
        FTSObj().RestAPIService.RestAPIServiceIP, #RestAPI IP
        FTSObj().SSLCoTService.SSLCoTServicePort, #SSLCoT Port
        FTSObj().SSLCoTService.SSLCoTServiceIP, #SSLCot IP
        True, #AutoStart
        True, #FirstStart
        False #UI
    )

@pytest.fixture(scope="session")
def fts_server():
    # Start FTS server process
    p = multiprocessing.Process(target=server_process)
    p.start()

    # Wait for server to spin up
    time.sleep(10)
    yield p
    p.terminate()

class TestDropPointComponent:

    @pytest.mark.asyncio
    async def test_drop_point_marker_2525(self, marker_2525_cot):
        client = PytakClient()
        result = await client.create_and_send_message(marker_2525_cot)
        assert len(result) == 1
        assert ''.join(result[0].decode().split()) == ''.join(ET.tostring(marker_2525_cot).decode().split())