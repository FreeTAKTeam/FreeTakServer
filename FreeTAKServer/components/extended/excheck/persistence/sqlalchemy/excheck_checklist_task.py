from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import ExcheckBase
from .excheck_checklist import ExCheckChecklist

class ExCheckChecklistTask(ExcheckBase):
    __tablename__ = "excheck_checklist_task"

    PrimaryKey = Column(String(100), primary_key=True)

    checklist_uid = Column(String, ForeignKey(ExCheckChecklist.PrimaryKey))

    checklist = relationship(ExCheckChecklist, back_populates="tasks")