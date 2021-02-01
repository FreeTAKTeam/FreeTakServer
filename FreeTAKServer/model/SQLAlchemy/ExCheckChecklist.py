from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import String
from sqlalchemy.orm import relationship
from FreeTAKServer.model.SQLAlchemy.ExCheck import ExCheck
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

class ExCheckChecklist(Base):
    __tablename__ = "ExCheckChecklist"
    PrimaryKey = Column(Integer, primary_key = True, autoincrement=True)
    startTime = Column(DateTime)
    creatorUid = Column(String)
    description = Column(String)
    name = Column(String)
    callsign = Column(String)
    uid = Column(String)
    filename = Column(String)
    template_id = Column(Integer, ForeignKey('ExCheck.PrimaryKey'))