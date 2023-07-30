from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .role_permission import RolePermission
    
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import MissionBase

class Permission(MissionBase):

    __tablename__ = "permission"
    
    permission_type: str = Column(String(100), primary_key=True) # type: ignore

    roles : List['RolePermission'] = relationship('RolePermission', back_populates="permission")