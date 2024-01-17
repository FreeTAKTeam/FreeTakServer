import json
import pathlib
from string import Template

COMPONENT_NAME = "cotmanager"

CONFIGURATION_FORMAT = "json"

BASE_OBJECT_NAME = "event"

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.parent.absolute()

CONFIGURATION_PATH_TEMPLATE = Template(
    str(
        pathlib.PurePath(
            CURRENT_COMPONENT_PATH, "configuration/model_definitions/$message_type"
        )
    )
    + f".{CONFIGURATION_FORMAT}"
)

LOGGING_CONFIGURATION_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/logging.conf")
)

ACTION_MAPPING_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH, "configuration/external_action_mapping.ini"
    )
)

INTERNAL_ACTION_MAPPING_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH, "configuration/internal_action_mapping.ini"
    )
)

TYPE_MAPPINGS = json.load(
    open(
        str(
            pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/type_mapping.json")
        ),
        "r",
        encoding="utf-8",
    )
)

COMPONENT_NAME_BUSINESS_RULES_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH,
        "configuration/business_rules/component_name_business_rules.json",
    )
)

PERSISTENCE_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "persistence/cotmanager.json")
)


