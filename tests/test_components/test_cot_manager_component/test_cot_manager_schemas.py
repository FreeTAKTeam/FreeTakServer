TEST_CONNECTION_SCHEMA = """
{
    "request": {
        "values": {
            "connection": {
                "oid": "3b1a979c-a31b-11ed-a8fc-0242ac120002",
                "service_id": "test_service",
                "protocol": "test_protocol",
                "is_node": true 
            }
        },
        "action": "connection"
    },
    "response": {
        "action": "publish",
        "values": {
            "message": [
                {
                    "is_node": true
                }
            ]
        }
    }
}
"""

TEST_GET_REPEATED_MESSAGES_SCHEMA = """
{
    "request": {
        "values": {},
        "action": "GetRepeatedMessages"
    },
    "response":{
        "action": "GetRepeatedMessages",
        "values": {
            "message": [
                {
                    "is_node": true
                }
            ]
        }
    }
}
"""

TEST_CREATE_REPEATED_MESSAGE_SCHEMA = """
{
    "request": {
        "values": {
            "message": [
                {
                    "oid": "59886b34-a31e-11ed-a8fc-0242ac120002",
                    "is_node": true
                }
            ]
        },
        "action": "CreateRepeatedMessage"
    },
    "response": {
        "action": "CreateRepeatedMessage",
        "values": {
            "success": true
        }
    }
}
"""

TEST_DELETE_REPEATED_MESSAGE_SCHEMA = """
{
    "request": {
        "action": "DeleteRepeatedMessage",
        "values": {
            "ids": [
                "329f80aa-a2f8-11ed-a8fc-0242ac120002"
            ]
        }
    },
    "response": {
        "action": "DeleteRepeatedMessage",
        "values": {
            "success": true
        }
    }
}
"""

TEST_DELETE_NON_EXISTENT_REPEATED_MESSAGE_SCHEMA = """
{
    "request": {
        "action": "DeleteRepeatedMessage",
        "values": {
            "ids": ["329f80aa-a2f8-11ed-a8fc-0242ac120002"]
        }
    },
    "response": {
        "action": "DeleteRepeatedMessage",
        "values": {
            "success": true
        }
    }
}
"""


