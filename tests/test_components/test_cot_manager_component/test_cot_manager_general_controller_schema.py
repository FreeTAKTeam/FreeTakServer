import json

TEST_MISSION_COT = json.dumps(
    {
        "request": {
            "action": "mission_cot_added",
            "values": {
                "dictionary":{
                    "event": {
                        "detail": {
                            "contact": {
                                "@callsign": "test_callsign"
                            },
                            "marti": {
                                "dest": [
                                    {
                                        "@mission": "test_mission"
                                    }
                                ]
                            }
                        },
                        "point": {
                            "@lat": 1,
                            "@lon": 1
                        },
                        "@type": "a-n-G",
                        "@uid": "test_uid"
                    }
                },
            }
        },
        "response": {
            "action": "",
            "values": {
                
            }
        }
    }
)