from abc import ABC, abstractmethod
from typing import NewType, List
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
class SerializerAbstract(ABC):
    """ logic for interacting with FTSObjects and methods which should be available in all serializers"""

    __ftsObjectType = NewType('ftsObject', FTSProtocolObject)

    @abstractmethod
    def from_format_to_fts_object(self, object: type, FTSObject: Event) -> Event:
        raise NotImplementedError

    @abstractmethod
    def from_fts_object_to_format(self, FTSObject: Event) -> type:
        raise NotImplementedError

    @abstractmethod
    def _get_method_in_method_list(self, method_list: List[callable], expected_class_name: str) -> callable:
        raise NotImplementedError

    def _get_fts_object_var_setter(self, FTSObject: __ftsObjectType, variable_name: str, setterlist=None) -> list:
        """ return variable setter from object

            recursively search the provided FTSObject instance for
            the setter associated with the specified variable which will
            then be returned. if this is not found an attribute error will
            be raised
        """

        if setterlist is None:
            setterlist = []
        variables = vars(FTSObject)
        for key, value in variables.items():
            if '_'+FTSObject.__class__.__name__.lower()+'__' in key.lower():
                continue
            elif issubclass(type(value), FTSProtocolObject):
                getter = getattr(FTSObject, "get"+key)
                setterlist.extend(self._get_fts_object_var_setter(getter(), variable_name))
            elif isinstance(value, list):
                getter = getattr(FTSObject, "get" + key)
                setterlist.extend(self._get_fts_object_var_setter(getter(), variable_name))
            elif variable_name == key:
                setterlist.append(getattr(FTSObject, 'set' + key))
            else:
                pass

        return setterlist

    def _get_fts_object_var_getter(self, FTSObject: __ftsObjectType, variable_name: str, getterlist = None) -> list:
        """ return variable getter from object

            recursively search the provided FTSObject instance for
            the getter associated with the specified variable which will
            then be returned. if this is not available an attribute error will
            be raised
        """
        if getterlist is None:
            getterlist = []

        variables = vars(FTSObject)
        for key, value in variables.items():
            if '_'+FTSObject.__class__.__name__.lower()+'__' in key.lower():
                continue
            elif issubclass(type(value), FTSProtocolObject):
                getterlist.extend(self._get_fts_object_var_getter(value, variable_name))
            elif isinstance(value, list):
                getter = getattr(FTSObject, 'get'+key)
                getterlist.extend(self._get_fts_object_var_getter(getter(), variable_name))
            elif variable_name == key:
                getterlist.append(getattr(FTSObject, 'get' + variable_name))
            else:
                pass

        return getterlist