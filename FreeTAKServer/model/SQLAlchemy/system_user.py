from sqlalchemy import Column
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy import Boolean
from flask_login import UserMixin


class SystemUser(Base, UserMixin):

    __tablename__ = 'SystemUser'
    uid = Column(String(25), primary_key=True)
    name = Column(String(15), nullable=False)
    token = Column(String(30), nullable=True)
    password = Column(String(30), nullable=True)
    group = Column(String(15), default=True, nullable=True)
    certificate_package_name = Column(String(30), nullable=True, default=None)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def get_id(self):
        return self.uid

    def __repr__(self):
        return str(self.name)
