from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase

class Permission(MissionBase):

    __tablename__ = "permission"

    PrimaryKey = Column(String(100), primary_key=True)

    role_uid = Column(String, ForeignKey("role.PrimaryKey"))

    role = relationship("Role", back_populates="role_permissions")

    permission_type = Column(String(100))