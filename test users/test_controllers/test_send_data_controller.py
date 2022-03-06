from unittest import mock, TestCase
import unittest
from FreeTAKServer.controllers.SendDataController import SendDataController
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.FTSModel.Dest import Dest
from FreeTAKServer.model.SpecificCoT.SendGeoChat import SendGeoChat
from FreeTAKServer.model.SpecificCoT.SendOther import SendOther
from FreeTAKServer.model.SpecificCoT.Presence import Presence
from FreeTAKServer.model.User import User
from FreeTAKServer.model.TCPConnection import TCPConnection
from multiprocessing import Queue
import socket


class Test_TestSendDataController(TestCase):

    def test_send_data_in_queue_geochat_sending(self):
        processed_cot = SendGeoChat()
        
        mocked_send_data_controller = SendDataController()
        mocked_send_data_controller.geochat_sending = mock.MagicMock(return_value='geochat')
        geochat_sending_out = SendDataController.sendDataInQueue(mocked_send_data_controller, 'sender', processed_cot, 'clientInformationQueue', 'shareDataPipe', messages_to_core_count = 0)
        
        mocked_send_data_controller.geochat_sending.assert_called_once_with('clientInformationQueue', processed_cot, 'sender', 'shareDataPipe')
        self.assertEqual(geochat_sending_out, "geochat")
    
    def test_send_data_in_queue_specific_client_chat(self):
        processed_cot = SendOther()
        processed_cot.xmlString = "testString"
        processed_cot.modelObject = Event.GeoChat()
        processed_cot.modelObject.detail._chat.chatgrp.uid1 = "testuid"
        
        mocked_send_data_controller = SendDataController()
        mocked_send_data_controller.send_to_specific_client = mock.MagicMock(return_value='specific client')
        specific_cot_sending_out = SendDataController.sendDataInQueue(mocked_send_data_controller, 'sender', processed_cot, 'clientInformationQueue', 'shareDataPipe', messages_to_core_count = 0)
        
        mocked_send_data_controller.send_to_specific_client.assert_called_once_with('clientInformationQueue', processed_cot, 'sender', 'shareDataPipe')
        self.assertEqual(specific_cot_sending_out, 'specific client')

    def test_send_data_in_queue_specific_client_marti(self):
        processed_cot = SendOther()
        processed_cot.xmlString = "testString"
        processed_cot.modelObject = Event.Other()
        processed_cot.modelObject.detail.marti.dest.append(Dest("testuid"))
        
        mocked_send_data_controller = SendDataController()
        mocked_send_data_controller.send_to_specific_client = mock.MagicMock(return_value='specific client')
        specific_cot_sending_out = SendDataController.sendDataInQueue(mocked_send_data_controller, 'sender', processed_cot, 'clientInformationQueue', 'shareDataPipe', messages_to_core_count = 0)
        
        mocked_send_data_controller.send_to_specific_client.assert_called_once_with('clientInformationQueue', processed_cot, 'sender', 'shareDataPipe')
        self.assertEqual(specific_cot_sending_out, 'specific client')

    def test_send_data_in_queue_send_to_all(self):
        processed_cot = SendOther()
        processed_cot.xmlString = "testString"
        processed_cot.modelObject = Event.Connection()

        mocked_send_data_controller = SendDataController()
        mocked_send_data_controller.send_to_all = mock.MagicMock(return_value='all clients')
        specific_cot_sending_out = SendDataController.sendDataInQueue(mocked_send_data_controller, 'sender', processed_cot, 'clientInformationQueue', 'shareDataPipe', messages_to_core_count = 0)
        
        mocked_send_data_controller.send_to_all.assert_called_once_with('clientInformationQueue', processed_cot, 'sender', 'shareDataPipe')
        self.assertEqual(specific_cot_sending_out, 'all clients')

    def test_send_to_specific_client_marti(self):
        client_sock = socket.socket
        client_sock.send = mock.MagicMock(return_value = None)
        client_con = TCPConnection()
        client_pres = Presence()
        client_pres.modelObject = Event.Presence()
        client_info = User(client_con, client_pres)
        client_info.m_presence.modelObject.detail.contact.callsign = "testcallsigndest"
        clientInformationQueue = {"testuidsource": [client_sock, client_info]}

        processed_cot = SendOther()
        processed_cot.xmlString = "testString"
        processed_cot.modelObject = Event.Other()
        processed_cot.modelObject.detail.marti.dest.append(Dest("testcallsigndest"))
        
        queue = Queue()
        queue.put = mock.MagicMock(return_value=None)

        mocked_send_data_controller = SendDataController()
        mocked_send_data_controller.messages_to_core_count = 0
        specific_cot_sending_out = SendDataController.send_to_specific_client(mocked_send_data_controller, clientInformationQueue, processed_cot, 'sender', queue)
        
        self.assertEqual(specific_cot_sending_out, 1)
        client_sock.send.assert_called_with(processed_cot.xmlString)
        queue.put.assert_called_once_with(processed_cot)

    def test_geochat_sending(self):
        self.client_sock = socket.socket
        self.client_sock.send = mock.MagicMock(return_value = None)
        self.clientInformationQueue = {"testuid": [self.client_sock]}

        processed_cot = SendOther()
        processed_cot.xmlString = "testString"
        processed_cot.modelObject = Event.GeoChat()
        processed_cot.modelObject.detail._chat.chatgrp.uid1 = "testuid"
        
        queue = Queue()
        queue.put = mock.MagicMock(return_value=None)
        
        SendDataController().send_to_specific_client(self.clientInformationQueue, processed_cot, None, queue)
        
        self.client_sock.send.assert_called_with(processed_cot.xmlString)
        queue.put.assert_called_once_with(processed_cot)

if __name__ == '__main__':
    unittest.main()