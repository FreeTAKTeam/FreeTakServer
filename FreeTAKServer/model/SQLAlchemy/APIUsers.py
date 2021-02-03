from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import Integer
from sqlalchemy import String


class APIUsers(Base, Root):
    __tablename__ = 'APIUsers'

    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String, unique=True, nullable=False)
    Token = Column(String, unique=True, nullable=False)
