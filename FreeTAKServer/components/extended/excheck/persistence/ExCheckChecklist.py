from sqlalchemy import Column
from FreeTAKServer.components.extended.excheck.persistence.sqlalchemy.checklist_mission import ChecklistMission
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class ExCheckChecklist(Base):
    __tablename__ = "ExCheckChecklist"
    PrimaryKey = Column(Integer, primary_key = True, autoincrement=True)
    startTime = Column(DateTime)
    creatorUid = Column(String(100))
    description = Column(String(100))
    name = Column(String(100))
    callsign = Column(String(100))
    uid = Column(String(100))
    filename = Column(String(100))
    template_id = Column(Integer, ForeignKey('ExCheck.PrimaryKey'))
    related_missions = Column(String(100))