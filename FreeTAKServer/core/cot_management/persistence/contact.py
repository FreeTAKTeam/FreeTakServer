from typing import TYPE_CHECKING
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import CoTManagementBase

if TYPE_CHECKING:
    from .detail import Detail

class Contact(CoTManagementBase):
    __tablename__ = "Contact"

    uid: Mapped[str] = Column(String, ForeignKey("Detail.uid"), primary_key=True)  # type: ignore

    callsign: Mapped[str] = Column(String)  # type: ignore

    detail: Mapped['Detail'] = relationship("Detail", back_populates="contact")

    iconsetpath: Mapped[str] = Column(String)  # type: ignore

    sipAddress: Mapped[str] = Column(String)  # type: ignore

    emailAddress: Mapped[str] = Column(String)  # type: ignore

    xmppUsername: Mapped[str] = Column(String)  # type: ignore

    endpoint: Mapped[str] = Column(String)  # type: ignore

    name: Mapped[str] = Column(String)  # type: ignore

    phone: Mapped[str] = Column(String)  # type: ignore