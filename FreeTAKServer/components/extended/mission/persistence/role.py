from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .role_permission import RolePermission
    
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase

class Role(MissionBase):
    __tablename__ = "role"

    role_type = Column(String(100), primary_key=True)

    permissions: List['RolePermission'] = relationship('RolePermission', back_populates="role")