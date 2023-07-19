from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase
from .mission import Mission
from .role import Role
class Subscription(MissionBase):
    __tablename__ = "subscription"

    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)

    username:str = Column(String(1000)) # type: ignore
    
    createTime = Column(String(1000))
    
    role: Role = relationship("Role")
    
    role_id = Column(String(1000), ForeignKey("role.role_type"))
    
    token: str = Column(String(1000)) # type: ignore

    clientUid: str = Column(String(1000)) # type: ignore

    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))

    mission : Mission = relationship(Mission, back_populates="mission_subscriptions")