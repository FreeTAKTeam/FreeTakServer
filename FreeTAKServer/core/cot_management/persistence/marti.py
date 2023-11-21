from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import CoTManagementBase

from .dest import Dest

if TYPE_CHECKING:
    from .detail import Detail
    

class Marti(CoTManagementBase):
    __tablename__ = "Marti"

    uid: Mapped[str] = Column(String, ForeignKey("Detail.uid"), primary_key=True)  # type: ignore

    detail: Mapped['Detail'] = relationship("Detail", back_populates="marti")

    dest: Mapped['Dest'] = relationship("Dest", back_populates="marti")