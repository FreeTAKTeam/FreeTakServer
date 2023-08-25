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

TEST_NEW_MISSION_CONTENT_SCHEMA = json.dumps({
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

TEST_COT_CREATED_NOTIFICATION_SCHEMA = json.dumps({

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