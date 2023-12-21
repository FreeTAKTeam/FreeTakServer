import json
TEST_GET_ALL_SUBSCRIPTIONS_SCHEMA = json.dumps(
{
    "request": {
        {
        "action": "GetAllSubscriptions"
        },
    },
    "response": {
        "action": "GetAllSubscriptions",
        "values": {
            "message": [
                {
                    "is_node": True
                }
            ]
        }
    }
})
