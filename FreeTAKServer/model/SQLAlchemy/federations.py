from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import Column, String, Integer, UniqueConstraint, Boolean

class Federations(Base):
    __tablename__ = "Federations"
    id = Column(String(100), primary_key=True)
    name = Column(String(100), unique=True)
    address = Column(String(100))
    port = Column(String(100))
    status = Column(String(100), default="Disabled")
    reconnectInterval = Column(Integer, default=30)
    maxRetries = Column(Integer, default=0)
    federate = Column(String(100), default="")
    protocolVersion = Column(Integer, default=1)
    connectionStatus = Column(String(100), default="DISABLED")
    lastError = Column(String(100), nullable=True)
    fallBack = Column(String(100), nullable=True)

class ActiveFederations(Base):
    __tablename__ = "ActiveFederations"
    id = Column(String(100), primary_key=True)
    federate = Column(String(100), default="")
    address = Column(String(100))
    port = Column(Integer)
    initiator = Column(String(100))
    readCount = Column(Integer, default=0)
    processedCount = Column(Integer, default=0)