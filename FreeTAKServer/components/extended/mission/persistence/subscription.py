import datetime
from datetime import datetime as dt
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import MissionBase
from .mission import Mission
from .role import Role

class Subscription(MissionBase):
    __tablename__ = "subscription"

    PrimaryKey: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    username: Mapped[str] = Column(String(1000), default="anonymous") # type: ignore
    
    createTime: Mapped[dt] = Column(DateTime, default=datetime.datetime.utcnow)
    
    role: Mapped['Role'] = relationship("Role")
    
    role_id: Mapped[str] = Column(String(1000), ForeignKey("Role.role_type"))
    
    token: Mapped[str] = Column(String(1000)) # type: ignore

    clientUid: Mapped[str] = Column(String(1000)) # type: ignore

    mission_uid: Mapped[str] = Column(String, ForeignKey(Mission.PrimaryKey))

    mission : Mapped['Mission'] = relationship(Mission, back_populates="mission_subscriptions")

    invitation: Mapped['MissionInvitation'] = relationship("MissionInvitation", back_populates="subscription")