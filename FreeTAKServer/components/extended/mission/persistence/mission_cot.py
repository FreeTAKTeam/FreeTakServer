from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .mission import Mission

from . import MissionBase

class MissionCoT(MissionBase):
    __tablename__ = "missioncot"
    
    uid = Column(String(100), primary_key=True)
    
    mission_uid: str = Column(String, ForeignKey(Mission.PrimaryKey)) # type: ignore

    mission : Mission = relationship(Mission, back_populates="cots")