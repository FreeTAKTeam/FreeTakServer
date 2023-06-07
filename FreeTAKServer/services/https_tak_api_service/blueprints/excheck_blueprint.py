from flask import Blueprint, request, make_response
from FreeTAKServer.components.extended.excheck.controllers.excheck_notification_controller import ExCheckNotificationController
from FreeTAKServer.services.https_tak_api_service.controllers.https_tak_api_communication_controller import HTTPSTakApiCommunicationController

page = Blueprint('Marti/api', __name__)

@page.route('/Marti/api/excheck/checklist/<checklistid>/task/<taskid>', methods=['PUT'])
def updatetemplate(checklistid, taskid):
    try:
        HTTPSTakApiCommunicationController().make_request("UpdateChecklistTask", "excheck", {"checklistuid": checklistid, "checklisttaskuid": taskid, "checklisttaskdata": request.data})
        HTTPSTakApiCommunicationController().make_request("ChecklistUpdateNotification", "excheck", {"task_uid": taskid, "changer_uid": "changeme"}, False, "tcp_cot_service")
        HTTPSTakApiCommunicationController().make_request("ChecklistUpdateNotification", "excheck", {"task_uid": taskid, "changer_uid": "changeme"}, False, "ssl_cot_service")
        return taskid, 200
        #dp_request = ObjectFactory.get_instance("request")
        #dp_response = ObjectFactory.get_instance("response")
        #excheck_facade = ObjectFactory.get_instance("ExCheck")
        #excheck_facade.initialize(dp_request, dp_response)
        #return excheck_facade.update_checklist_task(checklistuid=checklistid, checklisttaskuid=taskid, checklisttaskdata=request.data), 200
    except Exception as ex:
        print(ex)
        return '', 500

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
        dp_request = ObjectFactory.get_instance("request")
        dp_response = ObjectFactory.get_instance("response")
        excheck_facade = ObjectFactory.get_instance("ExCheck")
        excheck_facade.initialize(dp_request, dp_response)
        return excheck_facade.get_checklist(checklistuid=checklistid), 200
    except Exception as ex:
        print("exception in /Marti/api/excheck/checklist/ is "+str(ex))
        return '',500

@page.route('/Marti/api/excheck/<subscription>/start', methods=['POST'])
def startList(subscription):
    try:
        return HTTPSTakApiCommunicationController().make_request("StartChecklist", "excheck", {"templateuid":subscription, "checklistname":request.args.get("name"), "checklist_description":request.args.get("description")}).get_value("checklist")
        dp_request = ObjectFactory.get_instance("request")
        dp_response = ObjectFactory.get_instance("response")
        excheck_facade = ObjectFactory.get_instance("ExCheck")
        excheck_facade.initialize(dp_request, dp_response)
        return excheck_facade.start_checklist(templateuid=subscription, checklistname=request.args.get("name"), checklist_description=request.args.get("description")), 200
    except Exception as ex:
        print(ex)
        return '', 500
    
@page.route('/Marti/api/excheck/template', methods=['POST'])
def template():
    try:
        HTTPSTakApiCommunicationController().make_request("CreateTemplate", "excheck", {"templatedata": request.data}, None, False)
        return "done", 200
        dp_request = ObjectFactory.get_instance("request")
        dp_response = ObjectFactory.get_instance("response")
        excheck_facade = ObjectFactory.get_instance("ExCheck")
        excheck_facade.initialize(dp_request, dp_response)
        excheck_facade.create_template(request.data)
        return 'template created successfully', 200
        # return ExCheckController().template(PIPE)
    except Exception as ex:
        print(ex)
        return '', 500

@page.route('/Marti/api/missions/exchecktemplates', methods=['GET'])
@page.route('/Marti/api/missions/ExCheckTemplates', methods=['GET'])
def ExCheckTemplates():
    try:
        return HTTPSTakApiCommunicationController().make_request("GetAllTemplates", "excheck", {}).get_value("template_info")

        dp_request = ObjectFactory.get_instance("request")
        dp_response = ObjectFactory.get_instance("response")
        excheck_facade = ObjectFactory.get_instance("ExCheck")
        excheck_facade.initialize(dp_request, dp_response)
        return excheck_facade.get_all_templates(), 200
    except Exception as ex:
        print(ex)
        return '', 500
