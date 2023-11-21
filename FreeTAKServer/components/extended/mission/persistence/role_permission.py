from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from . import MissionBase
from .permission import Permission
from .role import Role

class RolePermission(MissionBase):
    __tablename__ = "role_permission"
    
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    
    permission_id: Mapped[str] = Column(String, ForeignKey(Permission.permission_type))
    permission: Mapped['Permission'] = relationship(Permission, back_populates="roles")
    
    role_uid: Mapped[str] = Column(String, ForeignKey(Role.role_type))
    role: Mapped['Role'] = relationship(Role, back_populates="permissions")