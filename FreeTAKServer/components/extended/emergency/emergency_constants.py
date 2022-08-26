from string import Template
import pathlib
import json

COMPONENT_NAME = 'Emergency'

CREATE_EMERGENCY_TYPE = "b-a-o-tbl"

DELETE_EMERGENCY_TYPE = "b-a-o-can"

CONFIGURATION_FORMAT = 'json'

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.absolute()

CONFIGURATION_PATH_TEMPLATE = Template(str(pathlib.PurePath(CURRENT_COMPONENT_PATH, 'configuration/$message_type'))+f'.{CONFIGURATION_FORMAT}')

LOGGING_CONFIGURATION_PATH = str(pathlib.PurePath(CURRENT_COMPONENT_PATH, 'configuration/logging.conf'))

ACTION_MAPPING_PATH = str(pathlib.PurePath(CURRENT_COMPONENT_PATH, 'configuration/emergency_action_mapping.ini'))

TYPE_MAPPINGS = json.load(open(str(pathlib.PurePath(CURRENT_COMPONENT_PATH, 'configuration/emergency_type_mapping.json')), 'r'))

BASE_OBJECT_NAME = 'Event'

EMERGENCY_ON = "emergency_on"

EMERGENCY_OFF = "emergency_delete"

EMERGENCY_ALERT = "emergency_alert"