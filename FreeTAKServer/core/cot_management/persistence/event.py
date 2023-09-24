from typing import List, TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import relationship

from . import CoTManagementBase

from .detail import Detail
from .point import Point

class Event(CoTManagementBase):
    __tablename__ = "Event"
    uid: str = Column(String(100), primary_key=True)  # type: ignore
    type: str = Column(String(100))  # type: ignore
    how: str = Column(String)  # type: ignore
    time: str = Column(String)  # type: ignore
    start: str = Column(String)  # type: ignore
    stale: str = Column(String)  # type: ignore

    detail: 'Detail' = relationship("Detail", back_populates="event", uselist=False)
    
    point: 'Point' = relationship("Point", back_populates="event", uselist=False)