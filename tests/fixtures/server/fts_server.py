import time
import multiprocessing
import pytest

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

@pytest.fixture(autouse=True, scope="session")
def fts_server():
    # Start FTS server process
    p = multiprocessing.Process(target=server_process)
    p.start()

    # Wait for server to spin up
    time.sleep(10)
    yield

    for child in multiprocessing.active_children():
        child.terminate()