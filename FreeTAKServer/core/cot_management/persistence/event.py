from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from . import CoTManagementBase

from .detail import Detail
from .point import Point

class Event(CoTManagementBase):
    __tablename__ = "Event"
    uid: Mapped[str] = Column(String(100), primary_key=True)  # type: ignore
    type: Mapped[str] = Column(String(100))  # type: ignore
    how: Mapped[str] = Column(String)  # type: ignore
    time: Mapped[str] = Column(String)  # type: ignore
    start: Mapped[str] = Column(String)  # type: ignore
    stale: Mapped[str] = Column(String)  # type: ignore

    detail: Mapped['Detail'] = relationship("Detail", back_populates="event", uselist=False)
    
    point: Mapped['Point'] = relationship("Point", back_populates="event", uselist=False)