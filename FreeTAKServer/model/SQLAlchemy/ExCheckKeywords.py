from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import String
from sqlalchemy import Integer

class ExCheckKeywords(Base):
    __tablename__ = 'ExCheckKeywords'
    PrimaryKey = Column(ForeignKey("ExCheckData.PrimaryKey"), primary_key = True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    callsign = Column(String)