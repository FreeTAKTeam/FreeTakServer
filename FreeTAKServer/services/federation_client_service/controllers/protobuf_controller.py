class ProtobufController:
    
    def process_protobuff_to_object(self, protobuf_object: FederatedEvent):
        """ this method will convert the protobuf object to a FTS model object and xml string
        it will also add the remarks to indicate that the client or cot is comming from a federate

        Args:
            protobuf_object:

        Returns:

        """
        model_object, fts_object = XMLCoTController().determine_model_object_type(protobuf_object.event.type)  # pylint: disable=no-member; member does exist
        fts_object = fts_object()
        model_object = ProtobufSerializer().from_format_to_fts_object(protobuf_object, model_object())
        xml_object = XmlSerializer().from_fts_object_to_format(model_object)
        fts_object.setModelObject(model_object)
        fts_object.setXmlString(etree.tostring(xml_object))
        """xmlstring = event
        if xmlstring.find('detail') and xmlstring.find('detail').
        xmlstring.find('detail').remove(xmlstring.find('detail').find('remarks'))
        xmlstring.find('detail').extend([child for child in xmlstring.find('detail')])"""
        return fts_object
    
    def get_header_length(self, header):
        return int.from_bytes(header, 'big')

    def generate_header(self, contentlength):
        return contentlength.to_bytes(4, byteorder="big")
