import pickle
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.hybrid import hybrid_property

from . import CoTManagementBase


class RepeatedMessage(CoTManagementBase):
    __tablename__ = "repeated_messages"
    
    id: str = Column(String, primary_key=True) # type: ignore
    
    message_contents: bytes = Column(LargeBinary, nullable=False) # type: ignore
    
    @hybrid_property
    def message(self):
        return pickle.loads(self.message_contents)