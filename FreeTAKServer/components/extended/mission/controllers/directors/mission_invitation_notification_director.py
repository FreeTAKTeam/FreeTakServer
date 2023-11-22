from abc import ABC
from typing import List, TYPE_CHECKING
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_content_change_builder import MissionContentChangeBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_change_list_builder import MissionChangeListBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_external_data_change_builder import MissionExternalDataChangeBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_invitation_notification_builder import MissionInvitationNotificationBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_permission_builder import MissionPermissionBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_simple_change_builder import MissionSimpleChangeBuilder
from FreeTAKServer.components.extended.mission.controllers.builders.mission_simple_cot_change_builder import MissionSimpleCoTChangeBuilder
from FreeTAKServer.components.extended.mission.persistence.mission import Mission
from FreeTAKServer.components.extended.mission.persistence.mission_invitation import MissionInvitation
from FreeTAKServer.core.domain.node import Node

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration

if TYPE_CHECKING:
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject

class MissionInvitationNotificationDirector(Controller):
    """direct the building of mission changes"""
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request, response):
        super().initialize(request, response)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def construct(self, mission_invitation: MissionInvitation, config_loader, *args, **kwargs) -> Node:
        """construct a node from a mapped object"""
        mission_invitation_notification_builder = MissionInvitationNotificationBuilder(self.request, self.response, self.action_mapper, self.configuration)
        mission_invitation_notification_builder.initialize(self.request, self.response)
        mission_invitation_notification_builder.build_empty_object(config_loader, *args, **kwargs)
        mission_invitation_notification_builder.add_object_data(mission_invitation)
        mission_invitation_notification = mission_invitation_notification_builder.get_result()

        for permission in mission_invitation.subscription.role.permissions:
            mission_permission_builder = MissionPermissionBuilder(self.request, self.response, self.action_mapper, self.configuration)
            mission_permission_builder.initialize(self.request, self.response)
            mission_permission_builder.build_empty_object(config_loader, *args, **kwargs)
            mission_permission_builder.add_object_data(permission.permission)
            mission_invitation_notification.detail.mission.role.permissions.permission = mission_permission_builder.get_result()

        return mission_invitation_notification