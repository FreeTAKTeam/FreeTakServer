from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .role_permission import RolePermission
    
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped

from . import MissionBase

class Permission(MissionBase):

    __tablename__ = "permission"
    
    permission_type: Mapped[str] = Column(String(100), primary_key=True) # type: ignore

    roles: Mapped['RolePermission'] = relationship('RolePermission', back_populates="permission")