from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from FreeTAKServer.components.extended.mission.persistence.external_data import ExternalData
    from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent
    from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from .mission import Mission

from . import MissionBase


class MissionChange(MissionBase):
    __tablename__ = "mission_change"

    PrimaryKey: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True) # type: ignore

    type: Mapped[str] = Column(String(100))

    content_uid: Mapped[str] = Column(String(100))

    creator_uid: Mapped[str] = Column(String(100))

    server_time: Mapped[datetime] = Column(DateTime, default=datetime.utcnow) # type: ignore

    timestamp: Mapped[datetime] = Column(DateTime, default=datetime.utcnow) # type: ignore

    mission_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey)) # type: ignore

    mission : Mapped['Mission'] = relationship(Mission, back_populates="changes")
    
    content_resource_uid: Mapped[str] = Column(String(100), ForeignKey('mission_content.PrimaryKey'))

    content_resource: Mapped['MissionContent'] = relationship("MissionContent", back_populates="change")

    cot_detail_uid: Mapped[str] = Column(String(100), ForeignKey('MissionCoT.uid'))

    cot_detail: Mapped['MissionCoT'] = relationship("MissionCoT", back_populates="change")

    external_data_uid: Mapped[str] = Column(String(100), ForeignKey('external_data.id'))

    external_data: Mapped['ExternalData'] = relationship("ExternalData", back_populates="change")