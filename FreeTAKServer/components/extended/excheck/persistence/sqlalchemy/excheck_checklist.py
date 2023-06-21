from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from . import ExcheckBase

class ExCheckChecklist(ExcheckBase):
    __tablename__ = "excheck_checklist"

    PrimaryKey = Column(String(100), primary_key=True)

    tasks = relationship("ExCheckChecklistTask", back_populates="checklist")