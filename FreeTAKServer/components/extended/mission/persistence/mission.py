from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


if TYPE_CHECKING:
    from .mission_content import MissionContent
    from .mission_cot import MissionCoT
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

    createTime = Column(String(100), default="2023-02-22T16:06:26.979Z")

    # groups = Column(String(100), default=[])

    # externalData = Column(String(100), default=[])

    # feeds = Column(String(100), default=[])

    # mapLayers = Column(String(100), default=[])

    defaultRole = relationship("Role")
    
    defaultRole_id = Column(String(1000), ForeignKey("role.role_type"))

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
        
    logs = relationship("MissionLog", back_populates="mission")
    
    cots: List['MissionCoT'] = relationship("MissionCoT", back_populates="mission")