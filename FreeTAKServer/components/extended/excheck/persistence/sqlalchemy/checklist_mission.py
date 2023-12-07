from sqlalchemy import Column
from . import ExcheckBase
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .excheck_checklist import ExCheckChecklist

class ChecklistMission(ExcheckBase):
    __tablename__ = "checklist_mission"

    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)

    mission_uid = Column(String(100))

    checklist_uid = Column(String, ForeignKey(ExCheckChecklist.PrimaryKey))

    checklist = relationship(ExCheckChecklist, back_populates="missions")