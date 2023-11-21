from .enterprise_sync_data_object import EnterpriseSyncDataObject

from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from FreeTAKServer.model.SQLAlchemy.Root import Base

class EnterpriseSyncKeyword(Base):
    """Table to store keywords"""

    __tablename__ = "keyword"
    id = Column(Integer, primary_key=True)
    keyword: Mapped[str] = Column(String(100)) # type: ignore
    
    enterprise_sync_data_object_id = Column(String(100), ForeignKey(EnterpriseSyncDataObject.PrimaryKey))
    enterprise_sync_data_object: Mapped['EnterpriseSyncDataObject'] = relationship(EnterpriseSyncDataObject, back_populates="keywords")