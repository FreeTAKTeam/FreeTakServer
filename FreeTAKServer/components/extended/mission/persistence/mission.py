from typing import TYPE_CHECKING, List
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


if TYPE_CHECKING:
    from .mission_content import MissionContent
    from .mission_change import MissionChange
    from .mission_cot import MissionCoT
    from .mission_log import MissionLog
    from .mission_to_mission import MissionToMission
    from .external_data import ExternalData
    
from . import MissionBase

class Mission(MissionBase):
    __tablename__ = "mission"

    PrimaryKey = Column(String(100), primary_key=True)

    name = Column(String(100), default="")
    
    description = Column(String(100), default="")

    chatRoom = Column(String(100), default="")

    baseLayer = Column(String(100), default="")

    bbox = Column(String(100), default="")

    path = Column(String(100), default="")

    classification = Column(String(100), default="")

    tool = Column(String(100), default="ExCheck")

    # keywords = Column(String(100), default=[])

    creatorUid = Column(String(100), default="")

    createTime: datetime = Column(DateTime, default=datetime.utcnow) # type: ignore

    # groups = Column(String(100), default=[])

    # feeds = Column(String(100), default=[])

    # mapLayers = Column(String(100), default=[])

    defaultRole = relationship("Role", back_populates="missions")
    
    defaultRole_id = Column(String(1000), ForeignKey("Role.role_type"))

    ownerRole = Column(String(100))

    inviteOnly = Column(String(100), default=False)

    expiration = Column(String(100), default=-1)

    guid = Column(String(100))

    uids = Column(String(100), default="[]")

    contents: List['MissionContent'] = relationship("MissionContent", back_populates="mission")

    token = Column(String(100))

    passwordProtected = Column(String(100), default=False)
    
    serviceUri = Column(String(100), default="")

    mission_items = relationship("MissionItem", back_populates="mission")

    mission_subscriptions = relationship("Subscription", back_populates="mission")
        
    externalData: List['ExternalData'] = relationship("ExternalData", back_populates="mission")
        
    logs: List['MissionLog'] = relationship("MissionLog", back_populates="mission")
    
    cots: List['MissionCoT'] = relationship("MissionCoT", back_populates="mission")

    changes: List['MissionChange'] = relationship("MissionChange", back_populates="mission")
    
    child_missions: List['MissionToMission'] = relationship("MissionToMission", back_populates="parent_mission", foreign_keys="[MissionToMission.parent_mission_id]")
    
    parent_missions: List['MissionToMission'] = relationship("MissionToMission", back_populates="child_mission", foreign_keys="[MissionToMission.child_mission_id]")