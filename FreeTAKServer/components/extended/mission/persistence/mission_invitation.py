from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from FreeTAKServer.components.extended.mission.persistence.subscription import Subscription

from .mission import Mission

from . import MissionBase

class MissionInvitation(MissionBase):
    __tablename__ = "MissionInvitation"
    
    uid: Mapped[str] = Column(String(100), primary_key=True)

    author_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore
    
    mission_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey), primary_key=True) # type: ignore

    subscription_uid: Mapped[str] = Column(String, ForeignKey(Subscription.PrimaryKey))

    subscription : Mapped['Subscription'] = relationship(Subscription, back_populates="invitation")