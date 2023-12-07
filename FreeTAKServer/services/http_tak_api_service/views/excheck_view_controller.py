from FreeTAKServer.services.https_tak_api_service.views.base_view_controller import BaseViewController


class ManageExcheckViewController(BaseViewController):

    def update_checklist_task(self, checklistuid, checklisttaskuid, checklisttaskdata):
        return_val = self.make_request("UpdateChecklistTask", {"checklistuid": checklistuid, "checklisttaskuid": checklisttaskuid, "checklisttaskdata": checklisttaskdata})
        self.make_request("ChecklistUpdateNotification", {"checklisttaskuid": checklisttaskuid}, False, "ssl_cot_service") # send the request output to the ssl cot service
        self.make_request("ChecklistUpdateNotification", {"checklisttaskuid": checklisttaskuid}, False, "tcp_cot_service") # send the request output to the ssl cot service
