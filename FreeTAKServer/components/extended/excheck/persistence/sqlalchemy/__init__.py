from sqlalchemy.orm import declarative_base

class ExcheckBase:
    __allow_unmapped__ = True

ExcheckBase = declarative_base(cls=ExcheckBase)
