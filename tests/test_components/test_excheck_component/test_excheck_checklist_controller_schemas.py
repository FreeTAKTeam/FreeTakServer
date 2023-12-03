import json

TEST_START_CHECKLIST_SCHEMA = json.dumps(
{
    "request": {
        "action": "StartChecklist",
        "values": {
            "templateuid": "test_template_uid",
            "checklistname": "test_checklist_name",
            "checklist_description": "test_checklist_description",
            "checklist_content": "",
        }
    }
}
)