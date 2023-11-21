from typing import TYPE_CHECKING, List
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
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

    PrimaryKey: Mapped[str] = Column(String(100), primary_key=True)

    name: Mapped[str] = Column(String(100), default="")
    
    description: Mapped[str] = Column(String(100), default="")

    chatRoom: Mapped[str] = Column(String(100), default="")

    baseLayer: Mapped[str] = Column(String(100), default="")

    bbox: Mapped[str] = Column(String(100), default="")

    path: Mapped[str] = Column(String(100), default="")

    classification: Mapped[str] = Column(String(100), default="")

    tool: Mapped[str] = Column(String(100), default="ExCheck")

    # keywords = Column(String(100), default=[])

    creatorUid: Mapped[str] = Column(String(100), default="")

    createTime: Mapped[datetime] = Column(DateTime, default=datetime.utcnow) # type: ignore

    # groups = Column(String(100), default=[])

    # feeds = Column(String(100), default=[])

    # mapLayers = Column(String(100), default=[])

    defaultRole: Mapped['Role'] = relationship("Role", back_populates="missions")
    
    defaultRole_id: Mapped[str] = Column(String(1000), ForeignKey("Role.role_type"))

    ownerRole: Mapped[str] = Column(String(100))

    inviteOnly: Mapped[str] = Column(String(100), default=False)

    expiration: Mapped[str] = Column(String(100), default=-1)

    guid: Mapped[str] = Column(String(100))

    uids: Mapped[str] = Column(String(100), default="[]")

    contents: Mapped['MissionContent'] = relationship("MissionContent", back_populates="mission")

    token: Mapped[str] = Column(String(100))

    passwordProtected: Mapped[str] = Column(String(100), default=False)
    
    serviceUri: Mapped[str] = Column(String(100), default="")

    mission_items: Mapped[str] = relationship("MissionItem", back_populates="mission")

    mission_subscriptions: Mapped[str] = relationship("Subscription", back_populates="mission")
        
    externalData: Mapped['ExternalData'] = relationship("ExternalData", back_populates="mission")
        
    logs: Mapped['MissionLog'] = relationship("MissionLog", back_populates="mission")
    
    cots: Mapped['MissionCoT'] = relationship("MissionCoT", back_populates="mission")

    changes: Mapped['MissionChange'] = relationship("MissionChange", back_populates="mission")
    
    child_missions: Mapped['MissionToMission'] = relationship("MissionToMission", back_populates="parent_mission", foreign_keys="[MissionToMission.parent_mission_id]")
    
    parent_missions: Mapped['MissionToMission'] = relationship("MissionToMission", back_populates="child_mission", foreign_keys="[MissionToMission.child_mission_id]")