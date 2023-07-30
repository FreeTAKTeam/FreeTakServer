from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import MissionBase
from .mission import Mission

class ExternalData(MissionBase):
    __tablename__ = 'external_data'
    
    id: int = Column(Integer, primary_key=True, autoincrement=True) # type: ignore
    
    name:str = Column(String) # type: ignore
    
    tool: str = Column(String) # type: ignore
    
    urlData: str = Column(String) # type: ignore
    
    notes: str = Column(String) # type: ignore
    
    uid: str = Column(String) # type: ignore
    
    urlView: str = Column(String) # type: ignore
    
    mission_uid = Column(String, ForeignKey(Mission.PrimaryKey))
    mission : Mission = relationship(Mission, back_populates="externalData")