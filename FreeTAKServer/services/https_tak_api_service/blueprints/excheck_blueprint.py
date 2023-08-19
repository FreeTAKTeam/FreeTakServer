from flask import Blueprint, request, make_response
from FreeTAKServer.components.extended.excheck.controllers.excheck_notification_controller import ExCheckNotificationController
from FreeTAKServer.services.https_tak_api_service.controllers.https_tak_api_communication_controller import HTTPSTakApiCommunicationController

page = Blueprint('Marti/api', __name__)

@page.route('/Marti/api/excheck/checklist/<checklistid>/task/<taskid>', methods=['PUT'])
def updatetemplate(checklistid, taskid):
    try:
        HTTPSTakApiCommunicationController().make_request("UpdateChecklistTask", "excheck", {"checklistuid": checklistid, "checklisttaskuid": taskid, "checklisttaskdata": request.data})
        HTTPSTakApiCommunicationController().make_request("ChecklistUpdateNotification", "excheck", {"task_uid": taskid, "changer_uid": "ANDROID-199eeda473669973"}, False, "tcp_cot_service")
        HTTPSTakApiCommunicationController().make_request("ChecklistUpdateNotification", "excheck", {"task_uid": taskid, "changer_uid": "ANDROID-199eeda473669973"}, False, "ssl_cot_service")
        return '', 200
    except Exception as ex:
        print(ex)
        return '', 500

@page.route('/Marti/api/excheck/checklist/<checklistid>/task/<taskid>', methods=['GET'])
def get_checklist_task(checklistid, taskid):
    return HTTPSTakApiCommunicationController().make_request("GetChecklistTask", "excheck", {"checklistuid": checklistid, "checklisttaskuid": taskid}, None, True).get_value("checklist_task_data"), 200

@page.route('/Marti/api/excheck/checklist/active', methods=["GET"])
def activechecklists():
    try:
        all_checklist_data = HTTPSTakApiCommunicationController().make_request("GetChecklists", "excheck").get_value("checklists")
        resp = make_response(all_checklist_data,200)
        resp.headers['Content-Type'] = "application/xml"
        return resp
    except Exception as ex:
        print(ex)
        return '', 500
    
@page.route('/Marti/api/excheck/checklist/<checklistid>')
def accesschecklist(checklistid):
    try:
        return HTTPSTakApiCommunicationController().make_request("GetChecklist", "excheck", {"checklistuid": checklistid}).get_value("checklist_data")
    except Exception as ex:
        print("exception in /Marti/api/excheck/checklist/ is "+str(ex))
        return '',500

@page.route('/Marti/api/excheck/<subscription>/start', methods=['POST'])
def startList(subscription):
    try:
        return HTTPSTakApiCommunicationController().make_request("StartChecklist", "excheck", {"templateuid":subscription, "checklistname":request.args.get("name"), "checklist_description":request.args.get("description")}).get_value("checklist")
    except Exception as ex:
        print(ex)
        return '', 500
    
@page.route('/Marti/api/excheck/template', methods=['POST'])
def template():
    try:
        HTTPSTakApiCommunicationController().make_request("CreateTemplate", "excheck", {"templatedata": request.data, "creator_uid": request.args.get("creatorUid", "")}, None, False)
        return "done", 200
    except Exception as ex:
        print(ex)
        return '', 500
    
@page.route('/Marti/api/excheck/template/<templateUid>', methods=['GET'])
def get_template(templateUid):
    try:
        return HTTPSTakApiCommunicationController().make_request("GetTemplate", "excheck", {"templateuid": templateUid}, None, False).get_value("template_data")
    except Exception as ex:
        print(ex)
        return '', 500

"""@page.route('/Marti/api/missions/exchecktemplates', methods=['GET'])
@page.route('/Marti/api/missions/ExCheckTemplates', methods=['GET'])
def ExCheckTemplates():
    try:
        return_val = HTTPSTakApiCommunicationController().make_request("GetAllTemplates", "excheck", {}, None, True).get_value("template_info"), 200
        return return_val
    except Exception as ex:
        print(ex)
        return '', 500
""" 
def get_checklist_mission(mission_id):
    return HTTPSTakApiCommunicationController().make_request("GetChecklistMission", "excheck", {"checklist_id": mission_id}, None, True).get_value("mission_info")

@page.route('/Marti/api/excheck/template/<templateUid>/task/<taskUid>', methods=['GET', 'PUT','DELETE','POST'])
def excheck_template_task(templateUid, taskUid):
    if request.method == "GET":
        return HTTPSTakApiCommunicationController().make_request("GetExcheckTemplateTask", "excheck", {templateUid, taskUid, request.data}).get_value("task_data")
    elif request.method == "POST":
        HTTPSTakApiCommunicationController().make_request("CreateExcheckTemplateTask", "excheck", {templateUid, taskUid, request.data}, None, False)
        return "", 200



"""
# TODO: this needs to be moved out to the mission blueprint
@page.route('/Marti/api/missions/<mission_id>', methods=['GET'])
def get_checklist_mission(mission_id):
    return HTTPSTakApiCommunicationController().make_request("GetChecklistMission", "excheck", {"checklist_id": mission_id}).get_value("mission_info")
"""