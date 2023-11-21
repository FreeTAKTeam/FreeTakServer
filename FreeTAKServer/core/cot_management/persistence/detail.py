from typing import TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import CoTManagementBase

from .contact import Contact
from .usericon import Usericon
from .marti import Marti

if TYPE_CHECKING:
    from .event import Event
    

class Detail(CoTManagementBase):
    __tablename__ = "Detail"

    uid: Mapped[str] = Column(String, ForeignKey("Event.uid"), primary_key=True)  # type: ignore

    contact: Mapped['Contact'] = relationship("Contact", back_populates="detail", uselist=False)

    usericon: Mapped['Usericon'] = relationship("Usericon", back_populates="detail", uselist=False)
    
    marti: Mapped['Marti'] = relationship("Marti", back_populates="detail", uselist=False)

    xml_content: Mapped[str] = Column(String)  # type: ignore

    event: Mapped['Event'] = relationship("Event", back_populates="detail")