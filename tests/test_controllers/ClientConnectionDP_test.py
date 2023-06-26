import os
import shutil
import zipfile

from unittest import mock
from jinja2 import Template
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.util.certificate_generation import generate_standard_zip

def test_generate_standard_zip(tmpdir):
    # Create a temporary directory for the test
    temp_dir = str(tmpdir)
    os.chdir(temp_dir)

    # Define sample parameters
    server_address = "tak.countyfire.com"
    server_filename = "server.p12"
    user_filename = "Client.p12"
    cert_password = "5Tr0ngP@ssw0rd!"
    ssl_port = "8089"

    # Mock the necessary functions and objects
    mock_socket = mock.Mock()
    mock_socket.gethostname.return_value = "test-host"
    mock_socket.gethostbyname.return_value = "127.0.0.1"

    mock_open = mock.mock_open()

    # UUID4 is a function that generates a random 128-bit value
    mock_uuid = mock.Mock()
    mock_uuid.uuid4.return_value = "sample-uuid"

    mock_copyfile = mock.Mock()

    mock_zipfile = mock.Mock(spec=zipfile.ZipFile)

    # Patch the necessary functions and objects with the mocks
    with mock.patch("socket.gethostname", mock_socket.gethostname), \
         mock.patch("socket.gethostbyname", mock_socket.gethostbyname), \
         mock.patch("builtins.open", mock_open), \
         mock.patch("uuid.uuid4", mock_uuid.uuid4), \
         mock.patch("shutil.copyfile", mock_copyfile), \
         mock.patch("zipfile.ZipFile", mock_zipfile):

        # Call the function under test
        generate_standard_zip(server_address, server_filename, user_filename,
                              cert_password, ssl_port)

        # Assert the function behavior and generated files
        mock_open.assert_any_call("fts.pref", "w")
        mock_open.assert_any_call("manifest.xml", "w")
        mock_copyfile.assert_any_call("path/to/server.p12", "server.p12")
        mock_copyfile.assert_any_call("path/to/Client.p12", "Client.p12")
        mock_zipfile.assert_called_once()

        # Clean up the temporary directory
        shutil.rmtree(temp_dir)