from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import CoTManagementBase

if TYPE_CHECKING:
    from .marti import Marti

class Dest(CoTManagementBase):
    __tablename__ = "Dest"

    uid: Mapped[str] = Column(String, ForeignKey("Marti.uid"), primary_key=True)  # type: ignore

    marti: Mapped['Marti'] = relationship("Marti", back_populates="dest")

    callsign: Mapped[str] = Column(String)  # type: ignore
