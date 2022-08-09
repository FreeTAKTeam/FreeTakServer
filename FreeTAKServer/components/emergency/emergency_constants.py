from string import Template

CREATE_EMERGENCY_TYPE = "b-a-o-tbl"

DELETE_EMERGENCY_TYPE = "b-a-o-can"

CONFIGURATION_FORMAT = 'json'

CONFIGURATION_PATH_TEMPLATE = Template(fr"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\components\emergency\configuration\$message_type.{CONFIGURATION_FORMAT}")

BASE_OBJECT_NAME = 'Event'

EMERGENCY_ON = "emergency_on"

EMERGENCY_OFF = "emergency_off"