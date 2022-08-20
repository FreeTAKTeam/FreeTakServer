from .abstract_serializer import SerializerAbstract
from FreeTAKServer.model.FTSModel.Event import Event
from typing import NewType, List
from defusedxml import ElementTree as etree
from lxml.etree import Element   # pylint: disable=no-name-in-module
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController

import time


loggingConstants = LoggingConstants(log_name="FTS_XmlSerializer")
logger = CreateLoggerController("FTS_XmlSerializer", logging_constants=loggingConstants).getLogger()

loggingConstants = LoggingConstants()


class XmlSerializer(SerializerAbstract):
    """this class is responsible for converting XML to domain objects"""
    __exception_mapping_dict = {'_group': '__group', '_serverdestination': '__serverdestination', '__group': "_group", '__serverdestination': "_serverdestination", "chat": "__chat", "_chat": "__chat", "__chat": "_chat", "_video": "__video", "__video":"_video", "connectionentry":"ConnectionEntry"}
    __exception_mapping_dict_objs = {'_group': '__group', '__group': "_group", "chat": "__chat", "_chat": "__chat", '_serverdestination': '__serverdestination', "_video": "__video", "__video":"_video"}

    __ftsObjectType = NewType('ftsObject', FTSProtocolObject)

    def from_format_to_fts_object(self, object: str, FTSObject: Event) -> Event:
        """ convert xmlstring to fts_object
        this function takes as input an xmlstring and it's corresponding FTSObject
        all data from the xmlstring is transfered to the FTS object and returned
        :param object:
        :param FTSObject:
        :return: an instance of the FTS model
        """
        element = etree.XML(object)
        self._xml_subelement_to_fts_nested(FTSObject, element, object)
        return self._xml_attribs_to_fts_properties(FTSObject, element)

    def _xml_attribs_to_fts_properties(self, FTSObject, element):
        if element.text is not None:  # this statement handles instances where tags have text eg. <example> text </example>
            try:
                FTSObject.text = element.text
            except AttributeError as e:
                logger.info("the following property is missing from the FTS model missing cot: " + str(etree.tostring(element)) + " attr: "+str("INTAG")+" please open an issue on the FTS github page with this message so that we can address it in future releases")
        for key, var in element.attrib.items():  # this statement handles iterating through and applying all element attributes to the model
            try:
                setters = self._get_fts_object_var_setter(FTSObject, key)
                setter = self._get_method_in_method_list(setters, element.tag)
                setter(var)
            except AttributeError as e:
                logger.info("the following property is missing from the FTS model missing cot: " + str(etree.tostring(element)) + " attr: "+str(key)+" please open an issue on the FTS github page with this message so that we can address it in future releases")

        return FTSObject

    def _xml_subelement_to_fts_nested(self, FTSObject, element, object):
        for subelem in etree.XML(object).findall("*"):
            if subelem.tag in self.__exception_mapping_dict:
                subelem.tag = self.__exception_mapping_dict[subelem.tag]
            try:
                setters = self._get_fts_object_var_setter(FTSObject, subelem.tag)
                setter = self._get_method_in_method_list(setters, element.tag)
                getters = self._get_fts_object_var_getter(FTSObject, subelem.tag)
                getter = self._get_method_in_method_list(getters, element.tag)
                fts_obj = getter()
                setter(self.from_format_to_fts_object(etree.tostring(subelem), fts_obj))
            except AttributeError:
                logger.info("the following tag is missing from the FTS model, missing cot "+str(etree.tostring(element)) + " missing tag name: "+str(subelem.tag))

    def from_fts_object_to_format(self, FTSObject: Event, root: Element = None) -> Element:
        """ serialize a FTS_object to an etree Element
        this function takes as parameters any FTSObject and will convert
        into the cooresponding etree element which can be converted into
        an xmlstring or left as a python object
        :rtype: etree._Element
        :param FTSObject:
        :param root:
        :return:
        """
        if root is None:
            object_body = self._from_fts_object_to_format_body(FTSObject)
            root = object_body
        self._fts_object_nested_to_xml_tags(FTSObject, root)
        return self._fts_object_attrib_to_xml_attrib(FTSObject, root)

    def _fts_object_nested_to_xml_tags(self, FTSObject, root):
        for property_name in FTSObject.get_all_properties():
            value = getattr(FTSObject, property_name)
            if issubclass(type(value), FTSProtocolObject):
                updatedValue = self.from_fts_object_to_format(value, root.find(property_name))
                # required to map the names with underscores
                if property_name in self.__exception_mapping_dict_objs:
                    property_name = self.__exception_mapping_dict_objs[property_name]
                root.remove(root.find(property_name))
                root.append(updatedValue)
            elif isinstance(value, list) and not '_'+FTSObject.__class__.__name__.lower()+'__' in property_name.lower():
                index = 0
                for obj in value:
                    self.from_fts_object_to_format(obj, root.findall(property_name)[index])
                    index += 1

    def _fts_object_attrib_to_xml_attrib(self, FTSObject, root):
        if FTSObject.text != "":
            root.text = FTSObject.text
        # this if statement is meant to handle the edge case where the cot has no
        # defined model thus it has defaulted to an xml string in particular the 
        # core component called cot_router which acts as the default case for all
        # message types without an explicit component to handle them
        if hasattr(FTSObject, "xml_string"):
            root = FTSObject.xml_string

        for key, val in root.attrib.items():

            root.attrib[key] = getattr(FTSObject, key)
        return root

    def _get_method_in_method_list(self, method_list: List[callable], expected_class_name: str) -> callable:
        if expected_class_name.lower() in self.__exception_mapping_dict:
            expected_class_name = self.__exception_mapping_dict[expected_class_name.lower()]
        if len(method_list) == 1:
            return method_list[0]

        elif len(method_list) > 0:
            for method in method_list:
                # required due to pythons privacy conventions
                if method.__self__.__class__.__name__.lower() in self.__exception_mapping_dict:
                    name = self.__exception_mapping_dict[method.__self__.__class__.__name__.lower()]
                else:
                    name = method.__self__.__class__.__name__.lower()
                if name == expected_class_name.lower() or method.__self__.__class__.__name__.lower() == expected_class_name.lower():
                    return method
                else:
                    pass
            raise AttributeError(expected_class_name + ' does not have specified attribute')
        else:
            raise AttributeError(expected_class_name + ' does not have specified attribute')

    def _from_fts_object_to_format_body(self, FTSObject: __ftsObjectType) -> Element:
        """ converts FTS object to xml outline without data

        this method takes an FTSObject instance and converts it to an xml message
        without populating it with any actual data.

        :param FTSObject an instance of FTSObject to be serialized

        :return an etree element containing the outline of the xml object
        """
        # set object name to lowercase
        name = type(FTSObject).__name__
        name = name[0].lower() + name[1:]
        if name.lower() in self.__exception_mapping_dict:
            name = self.__exception_mapping_dict[name.lower()]
        # create object and get attributes as dict
        xmlobj = Element(name)
        variables = FTSObject.cot_attributes
        # iterate variables and create attributes
        for key, value in variables.items():
            if '_'+FTSObject.__class__.__name__.lower()+'__' in key.lower():
                continue
            if issubclass(type(value), FTSProtocolObject):
                try:
                    xmlobj.append(self._from_fts_object_to_format_body(value))
                except AttributeError:
                    pass
            # continues iteration over list type attributes
            elif isinstance(value, list):
                for obj in value:
                    xmlobj.append(self._from_fts_object_to_format_body(obj))
            # handles all other regular attributes
            elif value is not None:
                xmlobj.attrib[key] = ""
        z = etree.tostring(xmlobj)
        return xmlobj


'''xmlstring = '<event version="2.0" uid="ANDROID-R5CN70EYKQH" type="a-f-G-U-C" how="h-e" start="2020-12-24T18:16:22.325Z" time="2020-12-24T18:16:22.325Z" stale="2020-12-24T18:22:37.325Z"><detail><__group name="Teal" role="Team Member"/><status battery="76"/><takv version="4.2.0.4 (47e136dd).1607456856-CIV" platform="ATAK-CIV" device="SAMSUNG SM-N986U" os="29"/><track course="159.1462509079387" speed="0.0"/><contact callsign="SPAC3SLOTH" endpoint="*:-1:stcp" /><uid Droid="SPAC3SLOTH"/><precisionlocation altsrc="GPS" geopointsrc="GPS"/></detail><point le="9999999.0" ce="11.0" hae="178.84407323983876" lon="-76.675505" lat="39.664392"/></event>'
fts_obj = xml_serializer().from_format_to_fts_object(xmlstring, Event.Connection())
obj = xml_serializer().from_fts_object_to_format_body(Event.Connection())
obj = xml_serializer().from_fts_object_to_format(fts_obj, etree.tostring(obj))
print(etree.tostring(obj))
print(etree.tostring(obj).decode() == xmlstring)
finish = time.time()
print(finish-start)'''