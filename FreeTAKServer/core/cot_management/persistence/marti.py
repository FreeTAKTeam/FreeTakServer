from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import relationship

from . import CoTManagementBase

from .dest import Dest

if TYPE_CHECKING:
    from .detail import Detail
    

class Marti(CoTManagementBase):
    __tablename__ = "Marti"

    uid: str = Column(String, ForeignKey("Detail.uid"), primary_key=True)  # type: ignore

    detail: 'Detail' = relationship("Detail", back_populates="marti")

    dest: 'Dest' = relationship("Dest", back_populates="marti")