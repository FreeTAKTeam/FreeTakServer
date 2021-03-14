from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import Column, String, Integer, UniqueConstraint, Boolean

class Federations(Base):
    __tablename__ = "Federations"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    address = Column(String)
    port = Column(String)
    status = Column(String, default="Disabled")
    reconnectInterval = Column(Integer, default=30)
    maxRetries = Column(Integer, default=0)
    federate = Column(String, default="")
    protocolVersion = Column(Integer, default=1)
    connectionStatus = Column(String, default="DISABLED")
    lastError = Column(String, nullable=True)
    fallBack = Column(String, nullable=True)

class ActiveFederations(Base):
    __tablename__ = "ActiveFederations"
    id = Column(String, primary_key=True)
    federate = Column(String, default="")
    address = Column(String)
    port = Column(Integer)
    initiator = Column(String)
    readCount = Column(Integer, default=0)
    processedCount = Column(Integer, default=0)