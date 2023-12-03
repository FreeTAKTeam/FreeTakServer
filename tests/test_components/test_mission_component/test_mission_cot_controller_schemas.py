import json


TEST_MISSION_COT_ADDED_SCHEMA = json.dumps( {
    "request": {
        "action": "mission_cot_added",
        "values": {
            "mission_ids": ["test_mission"],
            "cot_type": "test_cot_type",
            "uid": "test_cot_uid",
            "callsign": "test_callsign",
            "iconset_path": "test_iconset_path",
            "lat": "1.0",
            "lon": "1.0",
            "xml_content": "<event></event>"
        }
    },
    "response": {
        "action": "",
        "values": {
        }
    }
})

TEST_GET_MISSION_COTS_SCHEMA = json.dumps( {

    "request": {
        "action": "get_mission_cots",
        "values": {
            "mission_id": "test_mission"
        }
    },
    "response": {
        "action": "",
        "values": {
            "cots": "<events><event></event><event></event></events>"
        }
    }

})