from sqlalchemy import Column, ForeignKey, String, Integer
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy.orm import relationship

class Connectionentry(Base):
    __tablename__ = "Connectionentry"
    OwnerPrimaryKey = Column(String(100), ForeignKey("_Video.PrimaryKey"))
    _Video = relationship("_Video", back_populates="Connectionentry")
    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)
    networkTimeout = Column(String(100))
    uid = Column(String(100))
    path = Column(String(100))
    protocol = Column(String(100))
    bufferTime = Column(String(100))
    address = Column(String(100))
    port = Column(String(100))
    roverPort = Column(String(100))
    rtspReliable = Column(String(100))
    ignoreEmbeddedKLV = Column(String(100))
    alias = Column(String(100))