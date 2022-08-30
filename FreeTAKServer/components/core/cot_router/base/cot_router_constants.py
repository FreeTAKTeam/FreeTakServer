from string import Template
import pathlib

CONFIGURATION_FORMAT = "json"

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.parent.absolute()

CONFIGURATION_PATH_TEMPLATE = Template(
    str(pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/$message_type"))
    + f".{CONFIGURATION_FORMAT}"
)

LOGGING_CONFIGURATION_PATH = pathlib.PurePath(
    CURRENT_COMPONENT_PATH, "configuration/logging.conf"
)

ACTION_MAPPING_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH, "configuration/cot_router_action_mapping.ini"
    )
)

INTERNAL_ACTION_MAPPING_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH, "configuration/internal_action_mapping.ini"
    )
)

BASE_OBJECT_NAME = "Event"

BASE_COT = "base_cot"
