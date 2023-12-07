from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from . import ExcheckBase
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .excheck_checklist_task import ExCheckChecklistTask
    from .checklist_mission import ChecklistMission
class ExCheckChecklist(ExcheckBase):
    __tablename__ = "excheck_checklist"

    PrimaryKey = Column(String(100), primary_key=True)

    missions: List['ChecklistMission'] = relationship('ChecklistMission', back_populates="checklist")
    
    tasks: List['ExCheckChecklistTask'] = relationship("ExCheckChecklistTask", back_populates="checklist")