from abc import ABC, abstractmethod
from typing import NewType
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject


class SerializerAbstract(ABC):
    """logic for interacting with FTSObjects and methods which should be available in all serializers"""

    __ftsObjectType = NewType("ftsObject", FTSProtocolObject)

    @abstractmethod
    def from_format_to_fts_object(self, object: type, FTSObject: Event) -> Event:
        raise NotImplementedError

    @abstractmethod
    def from_fts_object_to_format(self, FTSObject: Event) -> type:
        raise NotImplementedError

    def _get_fts_object_var_setter(
        self, FTSObject: __ftsObjectType, variable_name: str, setterlist=None
    ) -> callable:
        """return variable setter from object
        access the setter from an ftsobject by means of a recursive
        itteration over all sub attributes
        """

        """try:
            setter = getattr(FTSObject, "set" + variable_name)
            return setter
        except Exception as e:
            raise AttributeError("unknown setter requested")"""

        if setterlist is None:
            setterlist = []
        variables = vars(FTSObject)
        for key, value in variables.items():
            if "_" + FTSObject.__class__.__name__.lower() + "__" in key.lower():
                continue
            elif variable_name == key:
                setterlist.append(getattr(FTSObject, key))
            elif issubclass(type(value), FTSProtocolObject):
                getter = getattr(FTSObject, key)
                setterlist.extend(
                    self._get_fts_object_var_setter(getter(), variable_name)
                )
            # elif isinstance(value, list):
            #    setter = getattr(FTSObject, 'set' + key)
            #    setterlist.append(setter)
            else:
                pass

        return setterlist

    def _get_fts_object_var_getter(
        self, FTSObject: __ftsObjectType, variable_name: str, getterlist=None
    ) -> callable:
        """return variable getter from object

        access the getter from an ftsobject
        """
        """try:
            getter = getattr(FTSObject, 'get' + variable_name)
            return getter
        except Exception as e:
            raise AttributeError("unknown getter requested")"""
        if getterlist is None:
            getterlist = []

        variables = FTSObject.cot_attributes
        for key, value in variables.items():
            if "_" + FTSObject.__class__.__name__.lower() + "__" in key.lower():
                continue
            elif variable_name == key:
                return [getattr(FTSObject, variable_name)]

            elif issubclass(type(value), FTSProtocolObject):
                getterlist.extend(self._get_fts_object_var_getter(value, variable_name))

            # elif isinstance(value, list):
            #    getter = getattr(FTSObject, 'get'+key)
            #    getterlist.append(getter)

            else:
                pass

        return getterlist
