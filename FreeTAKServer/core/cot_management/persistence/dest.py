from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import relationship

from . import CoTManagementBase

if TYPE_CHECKING:
    from .marti import Marti

class Dest(CoTManagementBase):
    __tablename__ = "Dest"

    uid: str = Column(String, ForeignKey("Marti.uid"), primary_key=True)  # type: ignore

    marti: 'Marti' = relationship("Marti", back_populates="dest")

    callsign: str = Column(String)  # type: ignore
