from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import String
from sqlalchemy import Integer
from FreeTAKServer.model.SQLAlchemy.ExCheckKeywords import ExCheckKeywords
from sqlalchemy.orm import relationship


class ExCheckData(Base):
    __tablename__ = 'ExCheckData'
    PrimaryKey = Column(ForeignKey("ExCheck.PrimaryKey"), primary_key=True, autoincrement=True)
    filename = Column(String)
    mimeType = Column(String)
    name = Column(String)
    submissionTime = Column(String)
    submitter = Column(String)
    uid = Column(String)
    hash = Column(String, unique=True)
    size = Column(Integer)
    tool = Column(String)
    keywords = relationship("ExCheckKeywords", uselist=False, backref="ExCheckData", cascade="all, delete")
