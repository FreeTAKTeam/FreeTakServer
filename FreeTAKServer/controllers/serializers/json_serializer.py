from typing import List

from FreeTAKServer.controllers.serializers.serializer_abstract import SerializerAbstract
from FreeTAKServer.model.FTSModel.Event import Event


class JsonSerializer(SerializerAbstract):

    def from_format_to_fts_object(self, object: dict, FTSObject: Event) -> Event:
        for key, value in object.items():
            if isinstance(value, dict):
                self._handle_sub_dictionary(FTSObject, key, value)
            else:
                self._handle_attribute(FTSObject, key, value)
        return FTSObject

    def _handle_attribute(self, FTSObject, key, value, expected_class_name=None):
        # retrieve setter list
        setters = self._get_fts_object_var_setter(FTSObject, key)
        # get correct setter
        setter = self._get_method_in_method_list(setters, expected_class_name)
        # call setter
        setter(value)

    def _handle_sub_dictionary(self, FTSObject, name: str, value: dict):
        for key, value in value.items():
            if value is dict:
                self._handle_sub_dictionary(FTSObject, key, value)
            else:
                self._handle_attribute(FTSObject, key, value, name)

    def _get_method_in_method_list(self, method_list: List[callable], expected_class_name: str = None) -> callable:
        if len(method_list) == 1:
            return method_list[0]

        elif len(method_list) == 0:
            raise AttributeError(expected_class_name + ' does not have specified attribute')

        elif len(method_list) > 1 and expected_class_name is not None:
            for method in method_list:
                if method.__self__.__class__.__name__.lower() == expected_class_name.lower():
                    return method
                else:
                    pass
            raise AttributeError('invalid json')

        else:
            raise AttributeError('invalid json')

    def from_fts_object_to_format(self, FTSObject: Event) -> dict:
        # TODO: This is broken
        for key, value in object.items():
            getters = self._get_fts_object_var_getter(FTSObject, key)
            getter = self._get_method_in_method_list(getters, key)
            value = getter()
        return object_body


if __name__ == "__main__":
    getter = JsonSerializer().get_fts_object_var_getter(Event.Presence(), 'uid')
    print(getter())
