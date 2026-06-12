import pytest
from FreeTAKServer.core.configuration.MainConfig import MainConfig
 
@pytest.fixture(autouse=True)
def reset_main_config():
    """Ensure MainConfig starts fresh for each MainConfig unit test."""
    MainConfig.reset()
    yield
