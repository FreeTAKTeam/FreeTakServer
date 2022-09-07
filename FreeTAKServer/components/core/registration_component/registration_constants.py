import pathlib


ROOT_COMPONENT_PATH = pathlib.Path(__file__).parent.parent.parent.absolute()

EXTENDED_COMPONENT_FOLDER_PATH = str(pathlib.PurePath(ROOT_COMPONENT_PATH, "extended"))

IMPORT_ROOT = "FreeTAKServer.components.extended"
