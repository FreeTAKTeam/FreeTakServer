from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import relationship

from . import CoTManagementBase

if TYPE_CHECKING:
    from .detail import Detail

class Contact(CoTManagementBase):
    __tablename__ = "Contact"

    uid: str = Column(String, ForeignKey("Detail.uid"), primary_key=True)  # type: ignore

    callsign: str = Column(String)  # type: ignore

    detail: 'Detail' = relationship("Detail", back_populates="contact")

    iconsetpath: str = Column(String)  # type: ignore

    sipAddress: str = Column(String)  # type: ignore

    emailAddress: str = Column(String)  # type: ignore

    xmppUsername: str = Column(String)  # type: ignore

    endpoint: str = Column(String)  # type: ignore

    name: str = Column(String)  # type: ignore

    phone: str = Column(String)  # type: ignore