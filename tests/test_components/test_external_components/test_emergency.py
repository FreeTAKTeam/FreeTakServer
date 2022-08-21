from digitalpy.core.impl.default_factory import DefaultFactory
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.core.object_factory import ObjectFactory
from unittest.mock import MagicMock
from FreeTAKServer.components.extended.emergency.emergency_constants import TYPE_MAPPINGS
from lxml import etree

def setup_module(module):
    config = InifileConfiguration("")
    config.add_configuration(r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\configuration\routing\action_mapping.ini")
    
    ObjectFactory.configure(DefaultFactory(config))
    ObjectFactory.register_instance('configuration', config)

    config.add_configuration(r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\components\core\cot_router\configuration\cot_router_action_mapping.ini")
    config.add_configuration(r"C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\components\extended\emergency\configuration\emergency_action_mapping.ini")

    request = ObjectFactory.get_new_instance('request')
    request.set_action("RegisterMachineToHumanMapping")
    request.set_value("machine_to_human_mapping", TYPE_MAPPINGS)
                
    actionmapper = ObjectFactory.get_instance('actionMapper')
    response = ObjectFactory.get_new_instance('response')
    actionmapper.process_action(request, response)
    
    request = ObjectFactory.get_new_instance('request')
    request.set_action("RegisterHumanToMachineMapping")
    # reverse the mapping and save the reversed mapping
    request.set_value("human_to_machine_mapping", {k: v for v, k in TYPE_MAPPINGS.items()})
                
    actionmapper = ObjectFactory.get_instance('actionMapper')
    response = ObjectFactory.get_new_instance('response')
    actionmapper.process_action(request, response)

def test_emergency_alert():
    test_data = '<event version="2.0" uid="S-1-5-21-2720623347-3037847324-4167270909-1002-9-1-1" type="b-a-o-tbl" time="2022-08-13T01:30:40.83Z" start="2022-08-13T01:30:40.83Z" stale="2022-08-13T01:40:40.83Z" how="h-e"><point lat="27.0196007365431" lon="-41.1839609383656" hae="9999999" ce="9999999" le="9999999" /><detail><link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" relation="p-p" /><contact callsign="DATA-Alert" /><emergency type="Alert">DATA</emergency></detail></event>'
    mock_message = MagicMock()
    mock_message.xmlString = test_data
    
    mock_client = MagicMock()
    
    request = ObjectFactory.get_new_instance('request')
    
    request.set_context('COT')
    request.set_action('b-a-o-tbl')
    request.set_value('message', mock_message)
    request.set_value('sender', '')
    request.set_value('clients', {'test': [mock_client, MagicMock()]})
    request.set_value('model_object_parser', "ParseModelObjectToXML")
    
    response = ObjectFactory.get_new_instance('response')
    actionmapper = ObjectFactory.get_instance('actionMapper')

    actionmapper.process_action(request, response)
    assert len(mock_client.send.call_args[0][0].decode()) == len(etree.tostring(etree.fromstring(test_data)))
    
def test_emergency_broadcast():
    test_data = '<event version="2.0" uid="S-1-5-21-2720623347-3037847324-4167270909-1002-9-1-1" type="b-a-o-tbl" time="2022-08-13T01:30:40.83Z" start="2022-08-13T01:30:40.83Z" stale="2022-08-13T01:40:40.83Z" how="h-e"><point lat="27.0196007365431" lon="-41.1839609383656" hae="9999999" ce="9999999" le="9999999" /><detail><link type="a-f-G-U-C-I" uid="S-1-5-21-2720623347-3037847324-4167270909-1002" relation="p-p" /><contact callsign="DATA-Alert" /><emergency type="Alert">DATA</emergency></detail></event>'
    mock_message = MagicMock()
    mock_message.xmlString = test_data
    
    mock_client = MagicMock()
    
    request = ObjectFactory.get_new_instance('request')
    request.set_action("EmergencyBroadcastAll")
    request.set_value("clients", {'test': [mock_client, MagicMock()]})
    request.set_value("model_object_parser", "ParseModelObjectToXML")
    request.set_value("sender", "")
    actionmapper = ObjectFactory.get_instance('actionMapper')
    response = ObjectFactory.get_new_instance('response')
    actionmapper.process_action(request, response)