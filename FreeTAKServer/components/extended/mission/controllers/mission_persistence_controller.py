import codecs
from datetime import datetime
from FreeTAKServer.components.extended.mission.persistence.log import Log

from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from ..configuration.mission_constants import PERSISTENCE_PATH
from digitalpy.core.main.controller import Controller
import json
import os
import pickle

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from ..persistence.role_permission import RolePermission
from ..persistence.permission import Permission
from ..persistence.role import Role
from ..persistence.subscription import Subscription
from ..persistence.mission_item import MissionItem
from ..persistence.mission_log import MissionLog
from ..persistence.log import Log
from ..persistence.mission import Mission
from ..persistence.mission_to_mission import MissionToMission
from ..persistence import MissionBase
from ..configuration.mission_constants import PERSISTENCE_PATH, DB_PATH, PERMISSIONS

class MissionPersistenceController(Controller):
    """this class is responsible for managing saved components"""

    def __init__(self, request, response, action_mapper, configuration):
        super().__init__(
        request=request,
        response=response,
        action_mapper=action_mapper,
        configuration=configuration,
    )
        super().__init__(request, response, action_mapper, configuration)
        self.ses = self.create_db_session()

    def initialize(self, request, response):
        super().initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def create_db_session(self) -> Session:
        """open a new session in the database

        Returns:
            Session: the session connecting the db
        """
        engine = create_engine(DB_PATH)
        # create a configured "Session" class
        SessionClass = sessionmaker(bind=engine)

        MissionBase.metadata.create_all(engine)

        # create a Session
        return SessionClass()

    def create_default_permissions(self, *args, **kwargs):
        """attempt to create the default permissions in the database
        """
        for permission_type in PERMISSIONS:
            if self.get_permission(permission_type) == None:
                try:
                    permission = Permission(
                        permission_type=permission_type,
                    )
                    self.ses.add(permission)
                    self.ses.commit()
                except Exception as ex:
                    self.ses.rollback()
                    raise ex
    
    def get_permission(self, permission_type, *args, **kwargs) -> Permission:
        """this method is used to get a permission from the database.
        """
        return self.ses.query(Permission).filter(Permission.permission_type == permission_type).first() # type: ignore
    
    def _initialize_role_permission(self, role: Role, permission: Permission, *args, **kwargs) -> RolePermission:
        """this method is used to create a role permission however it is NOT added to the database.
        """
        role_permission = RolePermission(
            role=role,
            permission=permission,
        )
        return role_permission
    
    def create_default_roles(self, *args, **kwargs):
        """attempt to create the default roles in the databases
        """
        try:
            if self.get_role("MISSION_OWNER") != None:
                return
            role = Role(
                role_type="MISSION_OWNER",
            )
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_SET_PASSWORD")))
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_MANAGE_LAYERS")))
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_WRITE")))
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_UPDATE_GROUPS")))
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_DELETE")))
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_SET_ROLE")))
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_READ")))
            self.ses.add(role)
            
            if self.get_role("MISSION_SUBSCRIBER") != None:
                return
            role = Role(
                role_type="MISSION_SUBSCRIBER",
            )
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_WRITE")))
            role.permissions.append(self._initialize_role_permission(role, self.get_permission("MISSION_READ")))
            self.ses.add(role)
            self.ses.commit()
            
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def get_role(self, role_type, *args, **kwargs) -> Role:
        """this method is used to get a role from the database.
        """
        try:
            role: Role = self.ses.query(Role).filter(Role.role_type == role_type).first() # type: ignore
            return role
        except Exception as ex:
            raise ex
    
    def create_subscription(self, subscription_id, mission_id, token, *args, **kwargs):
        """this method is used to create a new subscription and save it to the database.
        """
        try:
            subscription = Subscription()
            if subscription_id:
                subscription.PrimaryKey = subscription_id
            subscription.mission_uid = mission_id
            subscription.token = token
            self.ses.add(subscription)
            self.ses.commit()
            return subscription
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def get_subscription(self, subscription_id, *args, **kwargs) -> Subscription:
        """this method is used to get a subscription from the database.
        """
        try:
            subscription : Subscription = self.ses.query(Subscription).filter(Subscription.PrimaryKey == subscription_id).first() # type: ignore
            return subscription
        except Exception as ex:
            raise ex

    def update_subscription(self, subscription_id, role:Role = None, token: str= None, clientUid:str = None, username: str = None, *args, **kwargs): # type: ignore
        """this method is used to update a subscription in the database.
        """
        try:
            subscription = self.get_subscription(subscription_id)
            if role != None:
                subscription.role = role
            if token != None:
                subscription.token = token
            if clientUid != None:
                subscription.clientUid = clientUid
            if username != None:
                subscription.username = username
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def create_mission_item(self, mission_id, mission_item_id, mission_item_data, *args, **kwargs):
        """this method is used to create a new mission item and save it to the database.
        """
        try:
            mission_item = MissionItem()
            mission_item.PrimaryKey = mission_item_id
            mission_item.MissionItemData = mission_item_data
            mission_item.mission_uid = mission_id
            self.ses.add(mission_item)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex

    def get_mission_item(self, mission_item_id, *args, **kwargs):
        """this method is used to get a mission item from the database.
        """
        try:
            mission_item = self.ses.query(MissionItem).filter(MissionItem.PrimaryKey == mission_item_id).first()
            return mission_item
        except Exception as ex:
            raise ex
        
    def create_mission_content(self, mission_id: str, id: str) -> MissionContent:
        try:
            mission_content = MissionContent()
            mission_content.mission_uid = mission_id
            mission_content.PrimaryKey = id
            self.ses.add(mission_content)
            self.ses.commit()
            return mission_content
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def get_mission_content(self, id: str) -> MissionContent:
        try:
            mission_content: MissionContent = self.ses.query(MissionContent).filter(MissionContent.PrimaryKey == id).first() # type: ignore
            return mission_content
        except Exception as ex:
            raise ex

    def create_mission(self, mission_id, name, description, uids, contents, createTime, passwordProtected, groups, defaultRole, serviceUri, classification, *args, **kwargs):
        """this method is used to create a new mission, save it to the database and return the mission information
        to the client in json format, it uses the mission persistence controller to access the database.
        """
        try:
            mission = Mission()
            mission.PrimaryKey = mission_id
            mission.name = name
            mission.description = description
            #mission.uids = uids
            mission.createTime = createTime
            mission.passwordProtected = passwordProtected
            #mission.groups = groups
            mission.defaultRole = defaultRole
            mission.serviceUri = serviceUri
            mission.classification = classification
            self.ses.add(mission)
            self.ses.commit()
            return mission
        except Exception as ex:
            self.ses.rollback()
            raise ex
    
    def get_mission(self, mission_id, *args, **kwargs) -> Mission:
        """this method is used to get a mission from the database and return it to the client in json format.
        """
        try:
            mission: Mission = self.ses.query(Mission).filter(Mission.PrimaryKey == mission_id).first() # type: ignore
            return mission
        except Exception as ex:
            raise ex
        
    def add_parent_to_mission(self, child_mission:Mission, parent_mission: Mission, *args, **kwargs):
        try:
            mission_parent_rel: MissionToMission = MissionToMission()
                    
            mission_parent_rel.parent_mission = parent_mission
            mission_parent_rel.child_mission = child_mission
            
            child_mission.parent_missions.append(mission_parent_rel)
            parent_mission.child_missions.append(mission_parent_rel)
            
            self.ses.add(mission_parent_rel)
            
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def remove_parent_from_mission(self, mission_id, parent_mission: Mission, *args, **kwargs):
        try:
            mission: Mission = self.get_mission(mission_id)
            
            parent_mission_rel: MissionToMission = self.ses.query(MissionToMission).filter(MissionToMission.parent_mission_id == parent_mission.PrimaryKey).filter(MissionToMission.child_mission_id == mission.PrimaryKey).first() # type: ignore
            
            mission.parent_missions.remove(parent_mission_rel)
            
            parent_mission.child_missions.remove(parent_mission_rel)
            
            self.ses.delete(parent_mission_rel)
            
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def update_mission(self, mission_id: str, content: MissionContent = None, cot: MissionCoT = None, *args, **kwargs): #type: ignore
        try:
            mission: Mission = self.get_mission(mission_id)
            
            if content != None:
                mission.contents.append(content)
            if cot != None:
                mission.cots.append(cot)
                
            self.ses.commit()
            return mission
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def get_all_missions(self, *args, **kwargs):
        try:
            return self.ses.query(Mission).all()
        except Exception as ex:
            raise ex
        
    def create_mission_log(self, id, content, creatorUid, entryUid, mission, servertime, dtg, created, contentHashes, keywords, *args, **kwargs):
        """create a mission log record in the database"""
        try:
            mission_log = Log()
            mission_log.id = id
            mission_log.content = content
            mission_log.creatorUid = creatorUid
            mission_log.entryUid = entryUid
            mission_log.mission = mission
            mission_log.servertime = servertime
            mission_log.dtg = dtg
            mission_log.created = created
            mission_log.contentHashes = contentHashes
            mission_log.keywords = keywords
            self.ses.add(mission_log)
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def create_mission_cot(self, mission_id, uid):
        try:
            mission_cot = MissionCoT()
            mission_cot.uid = uid
            mission_cot.mission_uid = mission_id
            self.ses.add(mission_cot)
            self.ses.commit()
            return mission_cot
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def get_mission_logs(self, mission_id, *args, **kwargs):
        try:
            mission = self.get_mission(mission_id)
            return mission.logs
        except Exception as ex:
            raise ex
        
    def get_mission_logs_by_time(self, mission_id, start:datetime, end:datetime, *args, **kwargs):
        """get all mission logs since a specific time"""
        try:
            
            mission_logs = self.ses.query(MissionLog).join(Log, MissionLog.log_id == Log.id).filter(MissionLog.mission_uid == mission_id).filter(Log.created >= start).filter(Log.created <= end).all()
            return mission_logs
        except Exception as ex:
            raise ex
        
    def get_log(self, log_id:str) -> Log:
        try:
            log: Log = self.ses.query(Log).filter(Log.id == log_id).first() # type: ignore
            return log
        except Exception as ex:
            raise ex
        
    def create_log(self, uid, mission_ids, content, dtg, servertime, creatorUid, created, keywords, id) -> Log:
        try:
            log = Log()
            log.id = id
            log.entryUid = uid
            log.content = content
            log.creatorUid = creatorUid
            log.servertime = servertime
            log.dtg = dtg
            log.created = created
            log.keywords = keywords
            
            for mission_id in mission_ids:
                mission = self.get_mission(mission_id)
                mission_log = MissionLog()
                mission_log.mission = mission
                mission_log.log = log
                log.missions.append(mission_log)
                mission.logs.append(mission_log)
                self.ses.add(mission_log)
            self.ses.add(log)
            
            self.ses.commit()
            return log
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def update_log(self, id, entryUid=None, mission_ids=None, content=None, dtg=None, servertime=None, creatorUid=None, created=None, keywords=None) -> Log:
        try:
            log = self.get_log(id)
            if entryUid is not None:
                log.entryUid = entryUid
            if content is not None:
                log.content = content
            if creatorUid is not None:
                log.creatorUid = creatorUid
            if servertime is not None:
                log.servertime = servertime
            if dtg is not None:
                log.dtg = dtg
            if created is not None:
                log.created = created
            if keywords is not None:
                log.keywords = keywords

            if mission_ids is not None:
                for mission_id in mission_ids:
                    mission = self.get_mission(mission_id)
                    mission_log = MissionLog()
                    mission_log.mission = mission
                    mission_log.log = log
                    log.missions.append(mission_log)
                    mission.logs.append(mission_log)
                    self.ses.add(mission_log)
                
            self.ses.add(log)
            
            self.ses.commit()
            return log
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def delete_mission_log(self, log_id):
        try:
            self.ses.delete(self.get_log(log_id))
            self.ses.commit()
        except Exception as ex:
            self.ses.rollback()
            raise ex
        
    def get_all_logs(self):
        try:
            return self.ses.query(Log).all()
        except Exception as ex:
            raise ex