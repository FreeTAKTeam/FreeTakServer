from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from .mission import Mission
from . import MissionBase

class MissionItem(MissionBase):
    __tablename__ = "mission_item"

    PrimaryKey = Column(String(100), primary_key=True)

    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))

    mission = relationship(Mission, back_populates="mission_items")