import datetime
from datetime import datetime as dt
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase
from .mission import Mission
from .role import Role
class Subscription(MissionBase):
    __tablename__ = "subscription"

    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)

    username:str = Column(String(1000), default="anonymous") # type: ignore
    
    createTime: dt = Column(DateTime, default=datetime.datetime.utcnow)
    
    role: Role = relationship("Role")
    
    role_id = Column(String(1000), ForeignKey("Role.role_type"))
    
    token: str = Column(String(1000)) # type: ignore

    clientUid: str = Column(String(1000)) # type: ignore

    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))

    mission : Mission = relationship(Mission, back_populates="mission_subscriptions")

    invitation = relationship("MissionInvitation", back_populates="subscription")