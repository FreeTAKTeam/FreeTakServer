import os
import pathlib
import pytest

from tests.fixtures import *

pytest_plugins = [
    'tests.fixtures',
]

def pytest_collection(session):
    root = pathlib.Path(__file__).parent.parent.resolve()

    # Setup environment variables
    os.environ['FTS_MAINPATH'] = str(root)
    os.environ['FTS_EXCHECK_PATH'] = str(pathlib.PurePath(root, 'ExCheck'))
    os.environ['FTS_EXCHECK_CHECKLIST_PATH'] = str(pathlib.PurePath(root, 'ExCheck', 'checklist'))
    os.environ['FTS_EXCHECK_TEMPLATE_PATH'] = str(pathlib.PurePath(root, 'ExCheck', 'template'))

