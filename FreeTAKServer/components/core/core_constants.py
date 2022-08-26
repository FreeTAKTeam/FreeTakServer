import pathlib
import json

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.absolute()
TYPE_MAPPING_DB = json.load(str(pathlib.PurePath(CURRENT_COMPONENT_PATH, 'type_mapping.json')))