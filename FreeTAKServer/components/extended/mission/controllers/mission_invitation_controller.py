from FreeTAKServer.components.extended.mission.controllers.directors.mission_invitation_notification_director import MissionInvitationNotificationDirector
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.controllers.mission_subscription_controller import MissionSubscriptionController
from FreeTAKServer.components.extended.mission.controllers.directors.mission_invitation_list_director import MissionInvitationListDirector
from FreeTAKServer.core.util.serialization_utils import serialize_to_json
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.configuration.MainConfig import MainConfig


class MissionInvitationController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
        ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistence_controller = MissionPersistenceController(
            request, response, sync_action_mapper, configuration
        )
        self.invitation_notification_director = MissionInvitationNotificationDirector(
            request, response, sync_action_mapper, configuration
        )
        self.invitation_list_director = MissionInvitationListDirector(
            request, response, sync_action_mapper, configuration
        )
        self.subscription_controller = MissionSubscriptionController(
            request, response, sync_action_mapper, configuration
        )

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistence_controller.initialize(request, response)
        self.invitation_notification_director.initialize(request, response)
        self.invitation_list_director.initialize(request, response)
        self.subscription_controller.initialize(request, response)

    def get_invitations(self, client_uid: str, config_loader, *args, **kwargs):
        invitations = self.persistence_controller.get_client_invitations(client_uid)
        
        inivtation_model = self.invitation_list_director.construct(invitations, config_loader)

        serialized_change_collections = serialize_to_json(inivtation_model, self.request, self.execute_sub_action)

        self.response.set_value("mission_changes", serialized_change_collections)
        return serialized_change_collections


    def send_invitation(self, author_uid: str, client_uid: str, mission_id: str, config_loader, *args, **kwargs):
        self.subscription_controller.add_mission_subscription(client_uid, mission_id, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
        
        mission = self.persistence_controller.get_mission(mission_id)

        subscription = self.persistence_controller.get_subscription(mission, client_uid)
        
        db_invitation = self.persistence_controller.create_invitation(author_uid, subscription.PrimaryKey)

        invitation_notification = self.invitation_notification_director.construct(db_invitation, config_loader)


