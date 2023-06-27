import unittest
import pytest
import os
import zipfile

from unittest import mock
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.util.certificate_generation import generate_wintak_zip

def test_generate_wintak_zip(tmpdir):
    # Set up test data and temporary directory
    server_filename = "server.p12"
    user_filename = "Client.p12"
    cert_password = "5Tr0ngP@ssw0rd!"
    ssl_port = "8089"
    server_address = "192.168.205.117"
    tmpdir_path = str(tmpdir)


    # Call MainConfig class instance method to initialize and populate the _values dictionary
    MainConfig.instance()

    # Mock the necessary functions for file operations
    with mock.patch("FreeTAKServer.core.util.certificate_generation.os") as mock_os, \
            mock.patch("FreeTAKServer.core.util.certificate_generation.copyfile") as mock_copyfile:
        # Mock the os.path.exists function to return True for the temporary directory
        mock_os.path.exists.return_value = True

        # Call the function under test
        generate_wintak_zip(server_address=server_address, server_filename=server_filename,
                            user_filename=user_filename, cert_password=cert_password, ssl_port=ssl_port)

        # Assert that the expected file operations were performed
        mock_copyfile.assert_called_with(server_filename, os.path.join(tmpdir_path, server_filename))
        mock_copyfile.assert_called_with(os.path.join("cert", user_filename),
                                         os.path.join(tmpdir_path, user_filename))

        # Assert that the ZIP file was created with the expected contents
        zip_file_path = os.path.join(tmpdir_path, f"{user_filename[:-4]}.zip")
        assert os.path.exists(zip_file_path)
        with zipfile.ZipFile(zip_file_path) as zipf:
            assert "5c2bfcae3d98c9f4d262172df99ebac5/fts.pref" in zipf.namelist()
            assert "5c2bfcae3d98c9f4d262172df99ebac5/server.p12" in zipf.namelist()
            assert "5c2bfcae3d98c9f4d262172df99ebac5/Client.p12" in zipf.namelist()
            assert "MANIFEST/manifest.xml" in zipf.namelist()
            assert f"80b828699e074a239066d454a76284eb/{user_filename[:-4]}.zip" in zipf.namelist()