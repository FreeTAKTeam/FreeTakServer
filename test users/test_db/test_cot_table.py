from unittest import mock, TestCase

from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController

class Test_CoTTable(TestCase):
    def setUp(self) -> None:
        self.db_controller = DatabaseController()
        self.base_cot = Event.dropPoint()

    def test_create_cot(self):
        self.db_controller.create_CoT(self.base_cot)
    
    def test_basic_read_cot(self):
        query_output = self.db_controller.query_CoT(query=f"uid == '{self.base_cot.uid}'")
        assert len(query_output)>0

    def test_update_cot(self):
        self.db_controller.update_CoT(column_value = {"uid": "abc-123"}, query = f"uid=='{self.base_cot.uid}'")

    def test_delete_cot(self):
        self.db_controller.remove_CoT(query=f"uid == 'abc-123'")