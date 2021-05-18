from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base, Root
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

class APICalls(Base, Root):
    __tablename__ = 'APICalls'

    call_id = Column(Integer, primary_key = True, autoincrement=True)

    content = Column(String(10000), nullable=False)

    endpoint = Column(String(100), nullable=False)

    timestamp = Column(DateTime, nullable=False)

    user_id = Column(String(100), ForeignKey('SystemUser.uid'))
