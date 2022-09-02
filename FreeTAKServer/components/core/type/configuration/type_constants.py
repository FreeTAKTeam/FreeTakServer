import pathlib

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
