import json


TEST_NEW_MISSION_SCHEMA = json.dumps({
    "request": {
        "values": {
            "mission": ""
        },
        "action": "connection"
    },
    "response": {
        "action": "publish",
        "values": {
            "recipients": "*"
        }
    }
})