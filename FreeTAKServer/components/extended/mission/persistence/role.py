from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase

class Role(MissionBase):
    __tablename__ = "role"

    PrimaryKey = Column(String(100), primary_key=True)

    role_permissions = relationship("Permission", back_populates="role")

    role_type = Column(String(100))