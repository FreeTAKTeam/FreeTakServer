"""this package contains all the model objects, every model object class
should be defined as follows, _name.py containing a class Name with the class
exported here as Name. The class must be exported here as it is used by the
domain controller class (reference also model definition json file) to get classes based on the object configurations"""
from ._event import Event as Event
from ._component_property import componentproperty as componentproperty
