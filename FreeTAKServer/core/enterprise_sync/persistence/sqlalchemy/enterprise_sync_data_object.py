import datetime
import uuid
from datetime import datetime as dt
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .enterprise_sync_keyword import EnterpriseSyncKeyword

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, Sequence
from sqlalchemy.orm import relationship, Mapped

from FreeTAKServer.model.SQLAlchemy.Root import Base

class EnterpriseSyncDataObject(Base):
    __allow_unmapped__ = True
    """general object used to track all enterprise sync dataobjects
    so they can be indexed and found in the file system"""

    __tablename__ = "EnterpriseSyncDataObject"
    PrimaryKey = Column(String(100))
    id = Column(Integer, autoincrement=True, primary_key=True)
    file_type = Column(String(20))
    hash = Column(String(150))
    length = Column(Integer)
    
    keywords: Mapped['EnterpriseSyncKeyword'] = (
        relationship("EnterpriseSyncKeyword", back_populates='enterprise_sync_data_object', lazy="immediate"))
    
    start_time: dt = Column(DateTime, default=datetime.datetime.utcnow)
    submitter = Column(String(100), default="anonymous")
    expiration = Column(Integer, default=-1)
    mime_type = Column(String(100), default="")
    tool = Column(String(100), default="")
    creator_uid = Column(String(100), default="")
    file_name = Column(String(100), default="")
    private = Column(Integer, default=0)