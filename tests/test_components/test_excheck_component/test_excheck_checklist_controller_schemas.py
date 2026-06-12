import json

TEST_START_CHECKLIST_SCHEMA = json.dumps(
{
    "request": {
        "action": "StartChecklist",
        "values": {
            "templateuid": "test_template_uid",
            "checklistname": "test_checklist_name",
            "checklist_description": "test_checklist_description",
            "checklist_content": """
            <checklist>
                <checklistDetails>
                    <uid>test-checklist</uid>
                    <name>test</name>
                    <description>test</description>
                    <startTime>2025-01-01T00:00:00.000Z</startTime>
                </checklistDetails>
                <checklistTasks>
                </checklistTasks>
            </checklist>
            """,
        }
    },
    "response": {
        "action": None,
        "values": {}
    }
}
)