from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .enterprise_sync_keyword import EnterpriseSyncKeyword

from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship, backref

from .enterprise_sync_keyword import EnterpriseSyncKeyword

from FreeTAKServer.model.SQLAlchemy.Root import Base

class EnterpriseSyncDataObject(Base):
    """general object used to track all enterprise sync dataobjects
    so they can be indexed and found in the file system"""

    __tablename__ = "EnterpriseSyncDataObject"
    PrimaryKey = Column(String(100), primary_key=True)
    file_type = Column(String(20))
    hash = Column(String(150))
    length = Column(Integer)
    keywords: List['EnterpriseSyncKeyword'] = relationship("EnterpriseSyncKeyword", lazy="immediate")
    start_time = Column(String(100))
    submitter = Column(String(100), default="anonymous")
    expiration = Column(Integer, default=-1)
    mime_type = Column(String(100), default="")
    tool = Column(String(100), default="")
    creator_uid = Column(String(100))
    file_name = Column(String(100), default="")
    private = Column(Integer, default=0)