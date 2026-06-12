from sqlalchemy.orm import declarative_base

class MissionBase:
    __allow_unmapped__ = True

MissionBase = declarative_base(cls=MissionBase)
