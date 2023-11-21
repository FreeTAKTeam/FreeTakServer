from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from .mission import Mission
from . import MissionBase

class MissionItem(MissionBase):
    __tablename__ = "mission_item"

    PrimaryKey: Mapped[str] = Column(String(100), primary_key=True)

    mission_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey))

    mission: Mapped['Mission'] = relationship(Mission, back_populates="mission_items")