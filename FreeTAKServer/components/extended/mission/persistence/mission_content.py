from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange

from . import MissionBase
from .mission import Mission

class MissionContent(MissionBase):
    __tablename__ = "mission_content"
    
    PrimaryKey: Mapped[str] = Column(String(1000), primary_key=True) # type: ignore

    mission_uid: Mapped[str] = Column(String(1000), ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore

    mission : Mapped['Mission'] = relationship(Mission, back_populates="contents")

    change: Mapped['MissionChange'] = relationship("MissionChange", back_populates="content_resource")