from uuid import uuid4
from typing import TYPE_CHECKING
from FreeTAKServer.components.extended.mission.controllers.builders.mission_external_data_notification import MissionExternalDataNotificationBuilder
from FreeTAKServer.components.extended.mission.controllers.directors.mission_invitation_notification_director import MissionInvitationNotificationDirector

if TYPE_CHECKING:
    from FreeTAKServer.components.core.domain.domain import Event

from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.core.util.time_utils import get_dtg
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from FreeTAKServer.components.extended.mission.persistence.mission import Mission

class MissionNotificationController(Controller):
    def __init__(
        self, 
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration
    ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.domain_controller = MissionDomainController(request, response, sync_action_mapper, configuration)
        self.persistence_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)

    def send_mission_created_notification(self, mission_id: str, config_loader, *args, **kwargs):

        mission = self.persistence_controller.get_mission(mission_id)

        mission_creation_notification = self.domain_controller.create_mission_notification(config_loader)
        
        mission_creation_notification.uid = str(uuid4())
        mission_creation_notification.type = "t-x-m-n"
        mission_creation_notification.how = "h-g-i-g-o"
        mission_creation_notification.detail.mission.type = "CREATE"
        mission_creation_notification.detail.mission.tool = mission.tool
        mission_creation_notification.detail.mission.name = mission.name
        mission_creation_notification.detail.mission.authorUid = mission.creatorUid
        
        #notification_string = self.sample_notification(checklist_task_metadata.hash, update_task_model_object.stale, task_uid, update_task_model_object.start, len(checklist_task), checklist_task_obj.checklist_uid, checklist_element.find("checklistDetails").find("name").text, url, checklist_task)

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [mission_creation_notification])
        #self.response.set_value('message', [notification_string.encode()])
        
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")
    
    def send_log_created_notification(self, log_id: str, config_loader, *args, **kwargs):
        mission_log = self.persistence_controller.get_log(log_id)

        mission_log_notification = self.domain_controller.create_mission_notification(config_loader)
        
        mission_log_notification.uid = log_id
        mission_log_notification.type = "t-x-m-c-l"
        mission_log_notification.how = "h-g-i-g-o"
        mission_log_notification.detail.mission.type = "CHANGE"
        mission_log_notification.detail.mission.tool = mission_log.missions[0].mission.tool
        mission_log_notification.detail.mission.name = mission_log.missions[0].mission.name
        mission_log_notification.detail.mission.authorUid = mission_log.creatorUid
        
        #notification_string = self.sample_notification(checklist_task_metadata.hash, update_task_model_object.stale, task_uid, update_task_model_object.start, len(checklist_task), checklist_task_obj.checklist_uid, checklist_element.find("checklistDetails").find("name").text, url, checklist_task)

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [mission_log_notification])
        #self.response.set_value('message', [notification_string.encode()])
        
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")

    def send_content_created_notification(self, content_id: str, config_loader, *args, **kwargs):
        mission_change_db = self.persistence_controller.get_mission_change(content_id)

        mission_content_notification = self.domain_controller.create_mission_change_notification(config_loader)
        
        mission_change_record = self.domain_controller.create_mission_change_record(config_loader)

        mission_content_notification.uid = str(uuid4())
        mission_content_notification.type = "t-x-m-c"
        mission_content_notification.how = "h-g-i-g-o"
        mission_content_notification.detail.mission.type = "CHANGE"
        mission_content_notification.detail.mission.tool = mission_change_db.mission.tool
        mission_content_notification.detail.mission.name = mission_change_db.mission.name
        mission_content_notification.detail.mission.authorUid = mission_change_db.creator_uid
        
        self.domain_controller.complete_mission_change_notification(mission_content_notification, mission_change_db, config_loader)

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [mission_content_notification])
        
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")
    
    def send_external_data_created_notification(self, external_data_id: str, mission_id: str, config_loader, *args, **kwargs):
        mission_external_data_db = self.persistence_controller.get_external_data_by_uid(uid=external_data_id, mission_uid=mission_id)
        builder = MissionExternalDataNotificationBuilder(self.request, self.response, self.action_mapper, self.configuration)
        builder.build_empty_object(config_loader)
        builder.add_object_data(mission_external_data_db)
        mission_external_data_notification = builder.get_result()

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [mission_external_data_notification])
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")

    def send_external_data_updated_notification(self, external_data_id: str, mission_id: str, notes: str, config_loader, *args, **kwargs):
        mission_external_data_db = self.persistence_controller.get_external_data_by_uid(uid=external_data_id, mission_uid=mission_id)
        builder = MissionExternalDataNotificationBuilder(self.request, self.response, self.action_mapper, self.configuration)
        builder.build_empty_object(config_loader)
        builder.add_object_data(mission_external_data_db)
        mission_external_data_notification = builder.get_result()

        # the key difference between this and the create notification is that the notes are updated and urls have tokens
        token = uuid4()
        mission_external_data_notification.detail.mission.MissionChanges.MissionChange[0].externalData.urlData.text += f"?token={token}"
        mission_external_data_notification.detail.mission.MissionChanges.MissionChange[0].externalData.urlView.text += f"?token={token}"
        mission_external_data_notification.detail.mission.MissionChanges.MissionChange[0].externalData.notes.text = notes

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [mission_external_data_notification])
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")

    def send_invitation_notification(self, invitation_id: str, config_loader, *args, **kwargs):
        invitation_db = self.persistence_controller.get_invitation_id(invitation_id)
        director = MissionInvitationNotificationDirector(self.request, self.response, self.action_mapper, self.configuration)
        invitation_notification = director.construct(invitation_db, config_loader)

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [invitation_notification])
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")

    def send_cot_created_notification(self, mission_cot_id: str, config_loader, *args, **kwargs):
        mission_cot_db: MissionCoT = self.persistence_controller.get_mission_cot(mission_cot_id)
        self.request.set_value("cot_id", mission_cot_db.uid)
        cot_element: Event = self.execute_sub_action("GetCoT").get_value("cot")
        
        mission_cot_notification = self.domain_controller.create_mission_change_notification(config_loader)
        mission_cot_notification.detail.mission.MissionChanges.MissionChange[0].contentResource = None

        mission_cot_notification_details = self.domain_controller.create_details(config_loader)
        
        mission_cot_notification.detail.mission.MissionChanges.MissionChange[0].details = mission_cot_notification_details

        mission_cot_notification.uid = str(uuid4())
        mission_cot_notification.type = "t-x-m-c"
        mission_cot_notification.how = "h-g-i-g-o"
        mission_cot_notification.detail.mission.type = "CHANGE"
        mission_cot_notification.detail.mission.tool = mission_cot_db.mission.tool
        mission_cot_notification.detail.mission.name = mission_cot_db.mission.name
        mission_cot_notification.detail.mission.MissionChanges.MissionChange[0].contentUid.text = mission_cot_db.uid
        mission_cot_notification.detail.mission.MissionChanges.MissionChange[0].type.text = "ADD_CONTENT"
        mission_cot_notification.detail.mission.MissionChanges.MissionChange[0].isFederatedChange.text = "false"
        mission_cot_notification.detail.mission.MissionChanges.MissionChange[0].missionName.text = mission_cot_db.mission.name
        mission_cot_notification.detail.mission.MissionChanges.MissionChange[0].timestamp.text = cot_element.time

        self.domain_controller.complete_mission_cot_notification(mission_cot_notification_details, cot_element)

        # Serializer called by service manager requires the message value
        self.response.set_value('message', [mission_cot_notification])
        
        self.response.set_value('recipients', "*")
        self.response.set_action("publish")
