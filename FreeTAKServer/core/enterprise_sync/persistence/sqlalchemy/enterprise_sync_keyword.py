from sqlalchemy import Integer, String, Column
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from FreeTAKServer.model.SQLAlchemy.Root import Base


class EnterpriseSyncKeyword(Base):
    """Table to store keywords"""

    __tablename__ = "keyword"
    id = Column(Integer, primary_key=True)
    keyword = Column(String(100))
    enterprise_sync_data_object_id = Column(String(100), ForeignKey('EnterpriseSyncDataObject.PrimaryKey'))