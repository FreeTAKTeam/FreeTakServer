from FreeTAKServer.components.core.cot_router.cot_router_facade import COTRouterFacade
from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.object_factory import ObjectFactory
from unittest.mock import MagicMock
from lxml import etree

def setup_module(module):
    config = InifileConfiguration("")
    config.add_configuration(r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\configuration\routing\action_mapping.ini")
    
    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance('configuration', config)

    config.add_configuration(r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\components\core\cot_router\configuration\cot_router_action_mapping.ini")

def test_cot_received():
    test_data = '<event version="2.0" uid="3d331e11-7611-49a2-ba18-655995005627" type="a-f-G" how="h-g-i-g-o" time="2021-01-21T02:03:25Z" start="2021-01-21T02:03:25Z" stale="2022-01-21T02:03:25Z"> iieoidaoidwowa <point lat="39.3091185" lon="-29.1611324" hae="9999999" le="9999999" ce="9999999" /><detail><contact callsign="F.21.020325" /> <link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" parent_callsign="FAST" relation="p-p" production_time="2021-01-21T02:03:25Z" /><archive /><usericon iconsetpath="COT_MAPPING_2525B/a-f/a-f-G" /></detail></event>'
    mock_message = MagicMock()
    mock_message.xmlString = test_data
    
    mock_client = MagicMock()
    
    request = ObjectFactory.get_new_instance('request')
    
    request.set_context('COT')
    request.set_value('message', mock_message)
    request.set_value('sender', '')
    request.set_value('clients', {'test': [mock_client, MagicMock()]})
    request.set_value('model_object_parser', "ParseModelObjectToXML")
    
    response = ObjectFactory.get_new_instance('response')
    actionmapper = ObjectFactory.get_instance('actionMapper')

    actionmapper.process_action(request, response)
    assert len(mock_client.send.call_args[0][0].decode()) == len(etree.tostring(etree.fromstring(test_data)))
    
def test_cot_broadcast():
    pass