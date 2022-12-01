"""this package contains all the model objects, every model object class
should be defined as follows, _name.py containing a class Name with the class 
exported here as Name. The class must be exported here as it is used by the
domain controller class to get classes based on the object configurations"""
from ._event import Event as Event
from ._detail import detail as detail
from ._link import link as link
from ._contact import contact as contact
from ._emergency import emergency as emergency
from ._point import point as point
from ._remarks import remarks as remarks
from ._marti import marti as marti
from ._dest import dest as dest
