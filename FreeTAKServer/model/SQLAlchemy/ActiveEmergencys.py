from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from FreeTAKServer.model.SQLAlchemy.Root import Base


class ActiveEmergencys(Base):
    __tablename__ = 'ActiveEmergencys'

    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)
    event = relationship("Event")
    # event = relationship("Event", uselist=False, backref="ActiveEmergencys")
    uid = Column(String, ForeignKey('Event.uid'))
