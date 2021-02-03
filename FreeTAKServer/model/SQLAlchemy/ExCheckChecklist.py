from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base


class ExCheckChecklist(Base):
    __tablename__ = "ExCheckChecklist"
    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)
    startTime = Column(DateTime)
    creatorUid = Column(String)
    description = Column(String)
    name = Column(String)
    callsign = Column(String)
    uid = Column(String)
    filename = Column(String)
    template_id = Column(Integer, ForeignKey('ExCheck.PrimaryKey'))
