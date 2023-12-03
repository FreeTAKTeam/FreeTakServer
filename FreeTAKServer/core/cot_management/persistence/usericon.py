from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import relationship

from . import CoTManagementBase

if TYPE_CHECKING:
    from .detail import Detail

class Usericon(CoTManagementBase):
    __tablename__ = "Usericon"

    uid: str = Column(String, ForeignKey("Detail.uid"), primary_key=True)  # type: ignore

    detail: 'Detail' = relationship("Detail", back_populates="usericon")

    iconsetpath: str = Column(String)  # type: ignore