from typing import  TYPE_CHECKING

if TYPE_CHECKING:
    from .mission_log import MissionLog

from sqlalchemy import Column, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped

from . import MissionBase

class Log(MissionBase):
    __tablename__ = "log"
    id: Mapped[str] = Column(String(100), primary_key=True)  # type: ignore
    entryUid: Mapped[str] = Column(String(100))  # type: ignore
    content: Mapped[str] = Column(String)  # type: ignore
    creatorUid: Mapped[str] = Column(String)  # type: ignore
    servertime: Mapped[datetime] = Column(DateTime)  # type: ignore
    dtg: Mapped[datetime] = Column(DateTime)  # type: ignore
    created: Mapped[datetime] = Column(DateTime)  # type: ignore
    
    contentHashes: Mapped[str] = Column(String)  # type: ignore
    
    keywords: Mapped[str] = Column(String)  # type: ignore
    
    missions: Mapped['MissionLog'] = relationship("MissionLog", back_populates="log")
    