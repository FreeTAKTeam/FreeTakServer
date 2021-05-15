from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import VARCHAR
from sqlalchemy import CHAR
from sqlalchemy import DateTime
from datetime import datetime as dt

class APIUsers(Base, Root):
    __tablename__ = 'APIUsers'

    PrimaryKey = Column(Integer, primary_key = True, autoincrement=True)

    Username = Column(String(100), unique=True, nullable=False)

    Token = Column(String(100), unique=True, nullable=False)
