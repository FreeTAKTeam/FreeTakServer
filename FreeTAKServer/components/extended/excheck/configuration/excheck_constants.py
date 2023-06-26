import pathlib
from string import Template
from FreeTAKServer.core.configuration import MainConfig

TEMPLATE_CONTENT = "template_content"

TEMPLATE_METADATA = "template_metadata"

CHECKLIST_UPDATE = "checklist_update"

COMPONENT_NAME = "ExCheck"

CONFIGURATION_FORMAT = "json"

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.parent.absolute()

BASE_OBJECT = "base_object"

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

# TODO this path shouldn't be hardcoded, 
# find way to change this to a configured value.
LOG_FILE_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "logs")
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

BUSINESS_RULES_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/business_rules.json")
)

DB_PATH = "sqlite:///"+str(
    pathlib.PurePath(MainConfig.PERSISTENCE_PATH, "ExCheckRecords.db")
)

MANIFEST_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/manifest.ini")
)

BASE_OBJECT_NAME = "MissionInfo"

EVENT = "Event"