from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import CoTManagementBase

if TYPE_CHECKING:
    from .detail import Detail

class Usericon(CoTManagementBase):
    __tablename__ = "Usericon"

    uid: Mapped[str] = Column(String, ForeignKey("Detail.uid"), primary_key=True)  # type: ignore

    detail: Mapped['Detail'] = relationship("Detail", back_populates="usericon")

    iconsetpath: Mapped[str] = Column(String)  # type: ignore