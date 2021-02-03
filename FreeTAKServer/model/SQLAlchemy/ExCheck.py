from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from FreeTAKServer.model.SQLAlchemy.Root import Base


class ExCheck(Base):
    __tablename__ = 'ExCheck'
    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    creatorUid = Column(String)
    checklist = relationship("ExCheckChecklist", backref='template')
    data = relationship("ExCheckData", uselist=False, cascade="all, delete", backref="ExCheck")
