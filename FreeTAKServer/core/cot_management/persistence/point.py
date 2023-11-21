from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped

from . import CoTManagementBase
if TYPE_CHECKING:
    from .event import Event

class Point(CoTManagementBase):
    __tablename__ = "Point"
    uid: Mapped[str] = Column(String, ForeignKey("Event.uid"), primary_key=True)  # type: ignore

    event: Mapped['Event'] = relationship("Event", back_populates="point")

    lat: Mapped[float] = Column(Float)  # type: ignore

    lon: Mapped[float] = Column(Float)  # type: ignore

    hae: Mapped[float] = Column(Float)  # type: ignore

    ce: Mapped[float] = Column(Float)  # type: ignore

    le: Mapped[float] = Column(Float)  # type: ignore
