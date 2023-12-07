from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import ExcheckBase
from .excheck_template import ExCheckTemplate

class ExCheckTemplateTask(ExcheckBase):
    __tablename__ = "excheck_template_task"

    PrimaryKey = Column(String(100), primary_key=True)

    template_uid = Column(String, ForeignKey(ExCheckTemplate.PrimaryKey))

    template = relationship(ExCheckTemplate, back_populates="tasks")