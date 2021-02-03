#######################################################
#
# Event.py
# Python implementation of the Class Event
# Generated by Enterprise Architect
# Created on:      26-Sep-2020 12:18:51 PM
# Original author: natha
#
#######################################################
from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from FreeTAKServer.model.SQLAlchemy.CoTTables.Detail import Detail
from FreeTAKServer.model.SQLAlchemy.CoTTables.Point import Point
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Event(Base, Root):
    # default constructor  def __init__(self):

    __tablename__ = "Event"
    uid = Column(String, primary_key=True, unique=True)
    how = Column(String)
    start = Column(String)
    type = Column(String)
    version = Column(String)
    point = relationship("Point", uselist=False, backref="Event", cascade="all, delete, merge, delete-orphan")
    detail = relationship("Detail", uselist=False, backref="Event", cascade="all, delete, merge, delete-orphan")
