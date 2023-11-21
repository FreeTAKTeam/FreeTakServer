from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped

from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange

from .mission import Mission

from . import MissionBase

class ExternalData(MissionBase):
    __tablename__ = 'external_data'
    
    id: Mapped[int] = Column(String, primary_key=True) # type: ignore
    
    name: Mapped[str] = Column(String) # type: ignore
    
    tool: Mapped[str] = Column(String) # type: ignore
    
    urlData: Mapped[str] = Column(String) # type: ignore
    
    notes: Mapped[str] = Column(String) # type: ignore
    
    uid: Mapped[str] = Column(String) # type: ignore
    
    urlView: Mapped[str] = Column(String) # type: ignore
    
    mission_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey))
    mission: Mapped['Mission'] = relationship(Mission, back_populates="externalData")

    change: Mapped['MissionChange'] = relationship(MissionChange, back_populates="external_data")

    creator_uid: Mapped[str] = Column(String) # type: ignore