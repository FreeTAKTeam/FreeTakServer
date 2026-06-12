import json
TEST_GET_ALL_SUBSCRIPTIONS_SCHEMA = json.dumps(
{
    "request": {
        "action": "GetAllSubscriptions",
        "values": {}
    },
    "response": {
        "action": "GetAllSubscriptions",
        "values": {
            "mission_subscriptions": "{}"
        }
    }
})