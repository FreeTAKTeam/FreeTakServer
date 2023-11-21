from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange

from .mission import Mission

from . import MissionBase

class MissionCoT(MissionBase):
    __tablename__ = "MissionCoT"
    
    uid: Mapped[str] = Column(String(100), primary_key=True)
    
    mission_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore

    mission: Mapped['Mission'] = relationship(Mission, back_populates="cots")

    change: Mapped['MissionChange'] = relationship("MissionChange", back_populates="cot_detail")