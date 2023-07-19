import json
from typing import List, Dict
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_token_controller import MissionTokenController
from FreeTAKServer.components.extended.mission.domain.external_data import ExternalData
from FreeTAKServer.components.extended.mission.domain.mission_role import MissionRole
from FreeTAKServer.components.extended.mission.domain.mission_subscription import MissionSubscription
from FreeTAKServer.components.extended.mission.persistence.subscription import Subscription
from FreeTAKServer.core.domain.node import Node
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.configuration.MainConfig import MainConfig



from ..configuration.mission_constants import (
    BASE_OBJECT_NAME,
    MISSION_CONTENT,
    MISSION_ITEM,
    MISSION_SUBSCRIPTION,
    MISSION_NOTIFICATION
)

config = MainConfig.instance()


class MissionGeneralController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
        ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistency_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)
        self.token_controller = MissionTokenController(request, response, sync_action_mapper, configuration)
        self.domain_controller = MissionDomainController(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.token_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
 
    def put_mission(self, mission_id, mission_data: bytes, mission_data_args: Dict, creatorUid: str, config_loader, *args, **kwargs):
        """this method is used to create a new mission, save it to the database and return the mission information
        to the client in json format, it uses the mission persistence controller to access the database.
        """
        # wintak passes json in the body of the request, we need to convert it to a dictionary
        if mission_data != b'':
            initial_mission_data = json.loads(mission_data)
        # atak passes keyword arguments instead
        else:
            initial_mission_data = dict(mission_data_args)

        default_mission_role = self.persistency_controller.get_role(initial_mission_data.get('defaultRole'))

        mission_db_obj = self.persistency_controller.create_mission(
            str(mission_id),
            downloaded=str(initial_mission_data.get('downloaded')),
            connected=str(initial_mission_data.get('connected')),
            isSubscribed=str(initial_mission_data.get('isSubscribed')),
            autoPublish=str(initial_mission_data.get('autoPublish')),
            name=str(initial_mission_data.get('name')),
            description=str(initial_mission_data.get('description')),
            uids= str(initial_mission_data.get('uids')),
            contents=str(initial_mission_data.get('contents')),
            createTime=str(initial_mission_data.get('createTime')),
            passwordProtected=str(initial_mission_data.get('passwordProtected')),
            groups=str(initial_mission_data.get('groups')),
            defaultRole=default_mission_role,
            serviceUri=str(initial_mission_data.get('serviceUri')),
            classification=str(initial_mission_data.get('classification')),
            clientUid = creatorUid
        )
        
        token = self.token_controller.get_token(mission_db_obj)
        
        subscription_db_obj = self.persistency_controller.create_subscription(None, str(mission_id), token)    
        
        # set as owner because the default role for the creator of a mission should be owner
        self.persistency_controller.update_subscription(subscription_db_obj.PrimaryKey, role = self.persistency_controller.get_role("MISSION_OWNER"))
        
        self.persistency_controller.update_subscription(subscription_db_obj.PrimaryKey, clientUid = creatorUid)
        
        mission_collection_obj = self.domain_controller.create_mission_collection(config_loader)
        
        mission_subscription_obj = self.domain_controller.create_mission_record_object(config_loader)
        mission_subscription_obj = self.domain_controller.complete_mission_record_db(mission_subscription_obj, mission_db_obj, config_loader, subscription_db_obj)

        mission_collection_obj = self.domain_controller.add_mission_to_collection(mission_collection_obj, mission_subscription_obj)

        mission_notification_obj = self.domain_controller.create_mission_creation_notification(config_loader)
        mission_notification_obj = self.domain_controller.complete_mission_creation_notification(mission_notification_obj, mission_subscription_obj)
        
        final_message = self.serialize_to_json(mission_collection_obj)
        self.response.set_value("mission_subscription", final_message[0])
        
        serialized_mission_notification = self.serialize_to_xml(mission_notification_obj)
        
        self.response.set_value("message", serialized_mission_notification[0])
        # TODO: resolve these topics dynamically
        # tcp_cot_topic = f"/tcp_cot_service/XML/{self.response.get_sender()}/{self.response.get_context()}/{self.response.get_action()}/{self.response.get_id()}//{self.response.}".encode()
        # ssl_cot_topic = f"/ssl_cot_service/XML/{self.response.get_sender()}/{self.response.get_context()}/{self.response.get_action()}/{self.response.get_id()}/".encode()
        # source_topic = f"/{self.request.get_sender()}/XML/{self.response.get_sender()}/{self.response.get_context()}/{self.response.get_action()}/{self.response.get_id()}/".encode()
        # self.response.set_value("topics", [source_topic, tcp_cot_topic, ssl_cot_topic])
        return self.response

    def create_new_mission_notification(self, mission_id, creator_uid, config_loader, *args, **kwargs):
        """create a new mission notification object"""
        self.request.set_value("object_class_name", "Event")

        configuration = config_loader.find_configuration(MISSION_NOTIFICATION)

        self.request.set_value("configuration", configuration)

        self.request.set_value("extended_domain", {"mission": mission})

        self.request.set_value(
            "source_format", self.request.get_value("source_format")
        )
        self.request.set_value("target_format", "node")

        response = self.execute_sub_action("CreateNode")

        model_object = response.get_value("model_object")

        model_object.type = "t-x-m-n"
        model_object.how = "h-g-i-g-o"
        model_object.detail.mission.type = "CREATE"
        model_object.detail.mission.tool = "public"
        model_object.detail.mission.name = mission_id
        model_object.detail.mission.authorUid = creator_uid
        return model_object
        
    def create_mission_log(self, id, content, creator_uid, entry_uid, mission_id, servertime, dtg, created, content_hashes, keywords, *args, **kwargs):
        """create a new log entry for the mission
        Args:
            id (str): the id of the log entry
            content (str): the content of the log entry
            creator_uid (str): the uid of the creator of the log entry
            entry_uid (str): the uid of the log entry
            mission_id (str): the id of the mission
            servertime (str): the servertime of the log entry
            dtg (str): the dtg of the log entry
            created (str): the creation time of the log entry
            content_hashes (list): the content hashes of the log entry
            keywords (list): the keywords of the log entry
        """
        mission = self.persistency_controller.get_mission(mission_id)
        self.persistency_controller.create_mission_log(id, content, creator_uid, entry_uid, mission, servertime, dtg, created, content_hashes, keywords)
    
    def get_mission_logs(self):
        """get all mission logs in the db as json mission logs"""
        mission_logs_db = self.persistency_controller.get_all_mission_logs()
        mission_logs_domain = self.domain_controller.create_mission_logs(mission_logs_db)
        final_message = self.serialize_to_json(mission_logs_domain)
        self.response.set_value("mission_logs", final_message[0])
        return  final_message[0]
    
    def create_mission_content(self, mission_id, hashes=[], uids=[], *args, **kwargs):
        """create a new mission content object"""
        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData", objecthashs=hashes, objectuids=uids)
        mission_contents = sub_response.get_value("objectdata")
        for mission_content in mission_contents:
            self.persistency_controller.create_mission_content(mission_id, hash=mission_content.hash, uid=mission_content.uid)
    
    def get_missions(self, config_loader, *args, **kwargs):
        """get all missions on the server

        Args:
            config_loader (_type_): passed from the facade
        """
        missions = self.persistency_controller.get_all_missions()
        mission_collection = self.domain_controller.create_mission_collection(config_loader)
        for mission in missions:
            mission_record_domain = self.domain_controller.create_mission_record_object(config_loader)
            self.domain_controller.complete_mission_record_db(mission_record_domain, mission, config_loader)
            self.domain_controller.add_mission_to_collection(mission_collection, mission_record_domain)
        serialized_mission_collection = self.serialize_to_json(mission_collection)[0]    
        self.response.set_value("missions", serialized_mission_collection)
        return serialized_mission_collection

    def get_mission(self, mission_id: str, config_loader, *args, **kwargs):
        """get a specific mission by id"""
        mission = self.persistency_controller.get_mission(mission_id)
        mission_collection = self.domain_controller.create_mission_collection(config_loader)
        
        mission_record_domain = self.domain_controller.create_mission_record_object(config_loader)
        self.domain_controller.complete_mission_record_db(mission_record_domain, mission, config_loader)
        
        self.domain_controller.add_mission_to_collection(mission_collection, mission_record_domain)
        
        serialized_mission_collection = self.serialize_to_json(mission_collection)[0]    
        
        self.response.set_value("mission", serialized_mission_collection)
        return serialized_mission_collection
    
    def add_contents_to_mission(self, mission_id, config_loader, hashes=[], uids=[], *args, **kwargs):
        """add contents to a mission"""
        self.request.set_value("objecthashs", hashes)
        self.request.set_value("objectuids", uids)
        contents_metadata = self.execute_sub_action("GetMultipleEnterpriseSyncMetaData").get_value("objectmetadata")
        for metadata in contents_metadata:
            if metadata.hash != None:
                try:
                    content = self.persistency_controller.create_mission_content(mission_id, id=metadata.hash)
                    self.persistency_controller.update_mission(mission_id, content=content)
                except:
                    self.persistency_controller.get_mission_content(id=metadata.hash)
                hashes.remove(metadata.hash)
                
            elif metadata.PrimaryKey != None:
                content = self.persistency_controller.create_mission_content(mission_id, id=metadata.PrimaryKey)
                self.persistency_controller.update_mission(mission_id, content=content)
                uids.remove(metadata.PrimaryKey)
                
        for uid in uids:
            self.persistency_controller.create_mission_cot(mission_id, uid=uid)
        
        self.get_mission(mission_id, config_loader)
        
    def serialize_to_json(self, message: Node):
        self.request.set_value("protocol", "json")
        self.request.set_value("message", [message])
        response = self.execute_sub_action("serialize")
        return response.get_value("message")

    def serialize_to_xml(self, message: Node):
        self.request.set_value("protocol", "xml")
        self.request.set_value("message", [message])
        response = self.execute_sub_action("serialize")
        return response.get_value("message")
