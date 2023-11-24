import json

TEST_CREATE_TEMPLATE = json.dumps(
{
    "request": {
        "action": "StartChecklist",
        "values": {
            "creator_uid": "test_creator_uid",
            "templatedata": """
                <checklist>
                    <checklistColumns>
                        <checklistColumn>
                            <columnBgColor></columnBgColor>
                            <columnEditable>false</columnEditable>
                            <columnName>No.</columnName>
                            <columnTextColor></columnTextColor>
                            <columnType>LongString</columnType>
                            <columnWidth>0</columnWidth>
                        </checklistColumn>
                        <checklistColumn>
                            <columnBgColor></columnBgColor>
                            <columnEditable>false</columnEditable>
                            <columnName>Description</columnName>
                            <columnTextColor></columnTextColor>
                            <columnType>LongString</columnType>
                            <columnWidth>1</columnWidth>
                        </checklistColumn>
                    </checklistColumns>
                    <checklistDetails>
                        <missions/>
                        <creatorCallsign>DOWNFALL</creatorCallsign>
                        <creatorUid>ANDROID-199eeda473669973</creatorUid>
                        <description>a desc</description>
                        <name>myFirst</name>
                        <startTime>2023-09-05T19:27:48.080Z</startTime>
                        <templateName>myFirst</templateName>
                        <uid>5b5e2b3e-0f16-440f-9c47-e8981d2b4d56</uid>
                        <unreadCount>0</unreadCount>
                    </checklistDetails>
                    <checklistTasks>
                        <checklistTask>
                            <checklistUid>5b5e2b3e-0f16-440f-9c47-e8981d2b4d56</checklistUid>
                            <lineBreak>false</lineBreak>
                            <status>Pending</status>
                            <uid></uid>
                            <value>1</value>
                            <value>A</value>
                        </checklistTask>
                    </checklistTasks>
                </checklist>""",

        }
    },
    "response": {
        "action": "StartChecklist",
        "values": {
        }
    }
}
)