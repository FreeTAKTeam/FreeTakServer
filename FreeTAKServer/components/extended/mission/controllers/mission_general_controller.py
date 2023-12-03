import io
import json
from typing import List, Dict
import zipfile
from FreeTAKServer.components.extended.excheck.domain.mission_data import MissionData
from FreeTAKServer.components.extended.mission.controllers.directors.mission_director import MissionDirector
from FreeTAKServer.components.extended.mission.controllers.directors.mission_list_director import MissionListDirector
from FreeTAKServer.components.extended.mission.controllers.mission_change_controller import MissionChangeController
from FreeTAKServer.components.extended.mission.controllers.mission_external_data_controller import MissionExternalDataController
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_token_controller import MissionTokenController
from FreeTAKServer.components.core.domain.domain import mission
from FreeTAKServer.components.extended.mission.persistence.subscription import Subscription
from FreeTAKServer.core.domain.node import Node
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.util.serialization_utils import serialize_to_json
from FreeTAKServer.core.util.time_utils import get_datetime_from_dtg, get_current_datetime
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.main.object_factory import ObjectFactory

from FreeTAKServer.core.configuration.MainConfig import MainConfig



from ..configuration.mission_constants import (
    BASE_OBJECT_NAME,
    MISSION_CONTENT,
    MISSION_ITEM,
    MISSION_SUBSCRIPTION_DATA,
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
        self.external_data_controller = MissionExternalDataController(request, response, sync_action_mapper, configuration)
        self.change_controller = MissionChangeController(request, response, sync_action_mapper, configuration)
        self.mission_list_director = MissionListDirector(request, response, sync_action_mapper, configuration)
        self.mission_director = MissionDirector(request, response, sync_action_mapper, configuration)

    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.token_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.external_data_controller.initialize(request, response)
        self.change_controller.initialize(request, response)
        self.mission_list_director.initialize(request, response)
        self.mission_director.initialize(request, response)

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

        if isinstance(initial_mission_data.get('defaultRole'), dict):
            default_mission_role = self.persistency_controller.get_role(initial_mission_data['defaultRole']["type"])
        else:
            default_mission_role = self.persistency_controller.get_role(initial_mission_data.get('defaultRole'))

        if initial_mission_data.get('createTime', None) == None or get_datetime_from_dtg(str(initial_mission_data.get('createTime'))).year == 1:
            create_time = get_current_datetime()
        else:
            create_time = get_datetime_from_dtg(str(initial_mission_data.get('createTime')))

        mission_db_obj = self.persistency_controller.create_mission(
            str(mission_id),
            tool=str(initial_mission_data.get('tool', 'public')),
            downloaded=str(initial_mission_data.get('downloaded')),
            connected=str(initial_mission_data.get('connected')),
            isSubscribed=str(initial_mission_data.get('isSubscribed')),
            autoPublish=str(initial_mission_data.get('autoPublish')),
            name=str(mission_id),
            description=str(initial_mission_data.get('description')),
            uids= str(initial_mission_data.get('uids')),
            contents=str(initial_mission_data.get('contents')),
            createTime=create_time,
            passwordProtected=str(initial_mission_data.get('passwordProtected', 'False')),
            groups=str(initial_mission_data.get('groups')),
            defaultRole=default_mission_role,
            serviceUri=str(initial_mission_data.get('serviceUri')),
            classification=str(initial_mission_data.get('classification')),
            clientUid = creatorUid
        )
        
        token = self.token_controller.get_token(mission_db_obj)
        
        subscription_db_obj = self.persistency_controller.create_subscription(None, str(mission_id), token=token, client_uid=creatorUid, role=self.persistency_controller.get_role("MISSION_OWNER"))
        
        mission_obj = self.mission_director.construct(mission_db_obj, config_loader)

        mission_notification_obj = self.domain_controller.create_mission_notification(config_loader)
        mission_notification_obj = self.domain_controller.complete_mission_creation_notification(mission_notification_obj, mission_obj.data[0])
        
        final_message = serialize_to_json(mission_obj, self.request, self.execute_sub_action)
        
        self.response.set_value("mission_subscription", final_message)
        
        serialized_mission_notification = self.serialize_to_xml(mission_notification_obj)
        
        self.response.set_value("message", serialized_mission_notification[0])

        self.change_controller.create_mission_record(mission_id, creatorUid)
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
    
    def create_mission_content(self, mission_id, hashes=[], uids=[], *args, **kwargs):
        """create a new mission content object"""
        self.request.set_value("objecthashs", hashes)
        self.request.set_value("objectuids", uids)
        sub_response = self.execute_sub_action("GetMultipleEnterpriseSyncData")
        mission_contents = sub_response.get_value("objectdata")
        for mission_content in mission_contents:
            self.persistency_controller.create_mission_content(mission_id=mission_id, id=mission_content.uid)
    
    def get_missions(self, config_loader, *args, **kwargs):
        """get all missions on the server

        Args:
            config_loader (_type_): passed from the facade
        """
        missions = self.persistency_controller.get_all_public_missions()
        mission_collection = self.mission_list_director.construct(missions, config_loader)
        serialized_mission_collection = serialize_to_json(mission_collection, self.request, self.execute_sub_action) 
        #serialized_mission_collection = json.loads(serialized_mission_collection)
        #del serialized_mission_collection["data"][0]["externalData"][0]
        #serialized_mission_collection = json.dumps(serialized_mission_collection)
        self.response.set_value("missions", serialized_mission_collection)
        return serialized_mission_collection

    def get_mission(self, mission_id: str, config_loader, *args, **kwargs):
        """get a specific mission by id"""
        mission = self.persistency_controller.get_mission(mission_id)
        mission_obj = self.mission_director.construct(mission, config_loader)
        serialized_mission_collection = serialize_to_json(mission_obj, self.request, self.execute_sub_action)
        
        self.response.set_value("mission", serialized_mission_collection)
        return serialized_mission_collection
    
    def add_contents_to_mission(self, mission_id, config_loader, action_mapper, hashes=[], uids=[], *args, **kwargs):
        """add contents to a mission"""
        self.request.set_value("objecthashs", hashes)
        self.request.set_value("objectuids", uids)
        contents_metadata: List[EnterpriseSyncDataObject] = self.execute_sub_action("GetMultipleEnterpriseSyncMetaData").get_value("objectmetadata")
        self.request.set_value("use_bytes", True)
        contents_data = self.execute_sub_action("GetMultipleEnterpriseSyncData").get_value("objectdata")
        for metadata, data in zip(contents_metadata, contents_data):
            if metadata.mime_type == "application/x-zip-compressed":
                zipf = zipfile.ZipFile(io.BytesIO(data))
                file_data = zipf.open(zipf.filelist[0].filename).read()
                change_data = json.loads(zipf.open("changes.json").read())
                mission_changes = change_data['missionChanges'][0]['contentResource']

                sub_request = ObjectFactory.get_new_instance("request")
                sub_request.set_value("objectdata", file_data)
                sub_request.set_value("objectuid", mission_changes.get("uid", metadata.PrimaryKey))
                sub_request.set_value("objecthash", mission_changes.get("hash", metadata.hash))
                sub_request.set_value("synctype", "content")
                
                sub_request.set_value("objecthash", mission_changes.get("hash", metadata.hash))
                hashes.remove(metadata.hash)
                metadata.hash = mission_changes.get("hash", metadata.hash)
                hashes.append(metadata)

                sub_request.set_value("file_name", mission_changes.get("name", metadata.file_name))
                sub_request.set_value("mime_type", mission_changes.get("mimeType", metadata.mime_type))
                sub_request.set_value("objkeywords", mission_changes.get("keywords", metadata.keywords))
                sub_request.set_value("length", mission_changes.get("size", metadata.length))
                sub_request.set_value("objectuid", mission_changes.get("uid", metadata.PrimaryKey))
                sub_request.set_value("tool", "public")
                sub_request.set_value("privacy", 1)
                sub_request.set_action("SaveEnterpriseSyncData")
                
                sub_request.set_format("pickled")

                action_mapper.process_action(sub_request, self.response, False, protocol="json")
                
            if metadata.hash != None:
                content = self.persistency_controller.create_mission_content(mission_id, id=metadata.hash)
                self.persistency_controller.update_mission(mission_id, content=content)
                self.change_controller.create_mission_content_upload_record(mission_id, None, metadata.hash)
                hashes.remove(metadata.hash)
                
            elif metadata.PrimaryKey != None:
                content = self.persistency_controller.create_mission_content(mission_id, id=metadata.PrimaryKey)
                self.persistency_controller.update_mission(mission_id, content=content)
                self.change_controller.create_mission_content_upload_record(mission_id, None, metadata.PrimaryKey)
                uids.remove(metadata.PrimaryKey)
                
        #for uid in uids:
        #    self.persistency_controller.create_mission_cot(mission_id, uid=uid)

        self.get_mission(mission_id, config_loader)

    def serialize_to_xml(self, message: Node):
        self.request.set_value("protocol", "xml")
        self.request.set_value("message", [message])
        response = self.execute_sub_action("serialize")
        return response.get_value("message")
