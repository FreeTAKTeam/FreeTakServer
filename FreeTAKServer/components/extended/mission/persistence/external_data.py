from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange

from .mission import Mission

from . import MissionBase

class ExternalData(MissionBase):
    __tablename__ = 'external_data'
    
    id: int = Column(String, primary_key=True) # type: ignore
    
    name:str = Column(String) # type: ignore
    
    tool: str = Column(String) # type: ignore
    
    urlData: str = Column(String) # type: ignore
    
    notes: str = Column(String) # type: ignore
    
    uid: str = Column(String) # type: ignore
    
    urlView: str = Column(String) # type: ignore
    
    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))
    mission : Mission = relationship(Mission, back_populates="externalData")

    change: MissionChange = relationship(MissionChange, back_populates="external_data")

    creator_uid: str = Column(String) # type: ignore