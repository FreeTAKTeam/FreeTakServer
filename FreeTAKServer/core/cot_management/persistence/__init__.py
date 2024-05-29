from sqlalchemy.ext.declarative import declarative_base

class COTManagementBase:
    __allow_unmapped__ = True

CoTManagementBase = declarative_base(cls=COTManagementBase)
