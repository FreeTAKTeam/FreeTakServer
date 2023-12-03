from typing import List, TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Float
from datetime import datetime
from sqlalchemy.orm import relationship

from . import CoTManagementBase
if TYPE_CHECKING:
    from .event import Event

class Point(CoTManagementBase):
    __tablename__ = "Point"
    uid: str = Column(String, ForeignKey("Event.uid"), primary_key=True)  # type: ignore

    event: 'Event' = relationship("Event", back_populates="point")

    lat: float = Column(Float)  # type: ignore

    lon: float = Column(Float)  # type: ignore

    hae: float = Column(Float)  # type: ignore

    ce: float = Column(Float)  # type: ignore

    le: float = Column(Float)  # type: ignore
