from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .role_permission import RolePermission
    
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from . import MissionBase

class Role(MissionBase):
    __tablename__ = "Role"

    role_type: Mapped[str] = Column(String(100), primary_key=True)

    permissions: Mapped['RolePermission'] = relationship('RolePermission', back_populates="role")

    missions: Mapped['Mission'] = relationship("Mission", back_populates="defaultRole")