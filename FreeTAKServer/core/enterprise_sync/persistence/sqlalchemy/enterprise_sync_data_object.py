from sqlalchemy import String, Column

from FreeTAKServer.model.SQLAlchemy.Root import Base

class EnterpriseSyncDataObject(Base):
    """general object used to track all enterprise sync dataobjects
    so they can be indexed and found in the file system"""

    __tablename__ = "EnterpriseSyncDataObject"
    PrimaryKey = Column(String(100), primary_key=True)
    file_type = Column(String(20))
    hash = Column(String(150))