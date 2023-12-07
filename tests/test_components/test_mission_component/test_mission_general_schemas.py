import json


TEST_MISSION_CONTENT_SCHEMA = json.dumps({
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