import pathlib

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.absolute()

LOGGING_CONFIGURATION_PATH = str(pathlib.PurePath(CURRENT_COMPONENT_PATH, 'configuration/logging.conf'))