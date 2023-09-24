from typing import List, TYPE_CHECKING

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import relationship

from . import CoTManagementBase

from .contact import Contact
from .usericon import Usericon
from .marti import Marti

if TYPE_CHECKING:
    from .event import Event
    

class Detail(CoTManagementBase):
    __tablename__ = "Detail"

    uid: str = Column(String, ForeignKey("Event.uid"), primary_key=True)  # type: ignore

    contact: 'Contact' = relationship("Contact", back_populates="detail", uselist=False)

    usericon: 'Usericon' = relationship("Usericon", back_populates="detail", uselist=False)
    
    marti: 'Marti' = relationship("Marti", back_populates="detail", uselist=False)

    xml_content: str = Column(String)  # type: ignore

    event: 'Event' = relationship("Event", back_populates="detail")