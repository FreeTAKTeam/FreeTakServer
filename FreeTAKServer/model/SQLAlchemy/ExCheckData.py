from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import String
from sqlalchemy import Integer
from FreeTAKServer.model.SQLAlchemy.ExCheckKeywords import ExCheckKeywords
from sqlalchemy.orm import relationship

class ExCheckData(Base):
    __tablename__ = 'ExCheckData'
    PrimaryKey = Column(ForeignKey("ExCheck.PrimaryKey"), primary_key = True, autoincrement=True)
    filename = Column(String(100))
    mimeType = Column(String(100))
    name = Column(String(100))
    submissionTime = Column(String(100))
    submitter = Column(String(100))
    uid = Column(String(100))
    hash = Column(String(100), unique=True)
    size = Column(Integer)
    tool = Column(String(100))
    keywords = relationship("ExCheckKeywords", uselist=False, backref="ExCheckData", cascade="all, delete")