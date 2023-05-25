from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from . import ExcheckBase

class ExCheckTemplate(ExcheckBase):
    __tablename__ = "excheck_template"

    PrimaryKey = Column(String(100), primary_key=True)

    tasks = relationship("ExCheckTemplateTask", back_populates="template")