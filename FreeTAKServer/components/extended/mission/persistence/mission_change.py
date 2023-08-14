from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent
    from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT

from . import MissionBase
from .mission import Mission

class MissionChange(MissionBase):
    __tablename__ = "mission_change"

    PrimaryKey:str = Column(Integer, primary_key=True, autoincrement=True) # type: ignore

    type: str = Column(String(100))

    content_uid: str = Column(String(100))

    creator_uid: str = Column(String(100))

    server_time: datetime = Column(DateTime, default=datetime.utcnow) # type: ignore

    timestamp: datetime = Column(DateTime, default=datetime.utcnow) # type: ignore

    mission_uid: str = Column(String, ForeignKey(Mission.PrimaryKey)) # type: ignore

    mission : Mission = relationship(Mission, back_populates="changes")
    
    content_resource_uid = Column(String(100), ForeignKey('mission_content.PrimaryKey'))

    content_resource: 'MissionContent' = relationship("MissionContent", back_populates="change")

    #cot_detail_uid = Column(String(100), ForeignKey('MissionCoT.uid'))

    #cot_detail: 'MissionCoT' = relationship("MissionCoT", back_populates="change")