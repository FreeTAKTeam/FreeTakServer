from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import String
from sqlalchemy.orm import relationship
from FreeTAKServer.model.SQLAlchemy.ExCheckData import ExCheckData
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import ForeignKey


class ExCheck(Base):
    __tablename__ = 'ExCheck'
    PrimaryKey = Column(Integer, primary_key = True, autoincrement=True)
    timestamp = Column(DateTime)
    creatorUid = Column(String(100))
    checklist = relationship("ExCheckChecklist", backref='template')
    data = relationship("ExCheckData", uselist=False, cascade="all, delete", backref="ExCheck")
