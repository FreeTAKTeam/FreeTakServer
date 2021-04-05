from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import VARCHAR
from sqlalchemy import CHAR
from sqlalchemy import DateTime
from datetime import datetime as dt
from sqlalchemy.orm import relationship
from FreeTAKServer.model.SQLAlchemy.Event import Event
from sqlalchemy import ForeignKey

class ActiveEmergencys(Base):
    __tablename__ = 'ActiveEmergencys'

    PrimaryKey = Column(Integer, primary_key = True, autoincrement=True)

    event = relationship("Event")

    uid = Column(String(100), ForeignKey('Event.uid'))

    #event = relationship("Event", uselist=False, backref="ActiveEmergencys")
