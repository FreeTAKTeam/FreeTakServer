import pathlib

COMPONENT_NAME = "Domain"

CURRENT_COMPONENT_PATH = pathlib.Path(__file__).parent.parent.absolute()

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

SERIALIZATION_BUSINESS_RULES_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH,
        "configuration/business_rules/serialization_business_rules.json",
    )
)

DOMAIN_BUSINESS_RULES_PATH = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH,
        "configuration/business_rules/domain_business_rules.json",
    )
)

METRICS_ADDRESS = str(
    pathlib.PurePath(
        CURRENT_COMPONENT_PATH,
        "configuration/metrics.txt",
    )
)

MANIFEST_PATH = str(
    pathlib.PurePath(CURRENT_COMPONENT_PATH, "configuration/manifest.ini")
)

BASE_OBJECT_NAME = "event"
