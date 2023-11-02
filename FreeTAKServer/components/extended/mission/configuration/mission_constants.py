import json
import pathlib
from string import Template
from FreeTAKServer.core.configuration import MainConfig

COMPONENT_NAME = "mission"

CONFIGURATION_FORMAT = "json"

BASE_OBJECT_NAME = "MissionInfo"

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

LOG_FILE_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "logs")
)

DB_PATH = "sqlite:///"+str(
    pathlib.PurePath(MainConfig.PERSISTENCE_PATH, "MissionRecords.db")
)

MANIFEST_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/manifest.ini")
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
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "persistence/mission.json")
)

PERMISSIONS = [
    "MISSION_MANAGE_FEEDS",
    "MISSION_SET_PASSWORD",
    "MISSION_MANAGE_LAYERS",
    "MISSION_WRITE",
    "MISSION_UPDATE_GROUPS",
    "MISSION_DELETE",
    "MISSION_SET_ROLE",
    "MISSION_READ"
]

MISSION_CONTENT = "mission_content"

MISSION_ITEM = "mission_item"

MISSION_SUBSCRIPTION_DATA = "mission_subscription_data"

MISSION_SUBSCRIPTION = "mission_subscription"

MISSION_NOTIFICATION = "new_mission_notification"

MISSION_COLLECTION = "mission_collection"

MISSION_RECORD = "mission_record"

MISSION_SUBSCRIPTION_LIST = "mission_subscription_list"

MISSION_LOG = "mission_log"

MISSION_LOG_COLLECTION = "mission_log_collection"

MISSION_SUBSCRIPTION_SIMPLE_LIST = "mission_subscription_simple_list"

MISSION_EXTERNAL_DATA = "mission_external_data"

MISSION_EXTERNAL_DATA_COLLECTION = "mission_external_data"

MISSION_CHANGE_RECORD = "mission_change_record"

MISSION_CONTENT_DATA = "mission_content_data"

MISSION_CONTENT_NOTIFICATION= "mission_content_notification"

MISSION_CHANGES_OBJ = "mission_changes_obj"

MISSION_CHANGE_NOTIFICATION = "mission_change_notification"

MISSION_COT_CHANGE = "mission_cot_change"

MISSION_SIMPLE_COT_CHANGE = "mission_simple_cot_change"

MISSION_COT_CONTENT = "mission_cot_content"

MISSION_LIST_COT_CONTENT = "mission_list_cot_content"

MISSION_EXTERNAL_DATA_NOTIFICATION = "mission_external_data_notification"

EVENTS = "events"

DETAILS = "details"