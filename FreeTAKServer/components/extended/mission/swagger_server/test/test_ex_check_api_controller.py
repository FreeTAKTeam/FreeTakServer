# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.checklist import Checklist  # noqa: E501
from swagger_server.models.checklist_task import ChecklistTask  # noqa: E501
from swagger_server.test import BaseTestCase


class TestExCheckApiController(BaseTestCase):
    """ExCheckApiController integration test stubs"""

    def test_add_edit_checklist_task(self):
        """Test case for add_edit_checklist_task

        
        """
        body = ChecklistTask()
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}/task/{taskUid}'.format(checklist_uid='checklist_uid_example', task_uid='task_uid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_edit_template_task(self):
        """Test case for add_edit_template_task

        
        """
        body = ChecklistTask()
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/template/{templateUid}/task/{taskUid}'.format(template_uid='template_uid_example', task_uid='task_uid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_mission_reference_to_checklist(self):
        """Test case for add_mission_reference_to_checklist

        
        """
        query_string = [('client_uid', 'client_uid_example'),
                        ('password', 'password_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}/mission/{missionName}'.format(checklist_uid='checklist_uid_example', mission_name='mission_name_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_checklist(self):
        """Test case for create_checklist

        
        """
        body = Checklist()
        query_string = [('client_uid', 'client_uid_example'),
                        ('default_role', 'default_role_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_checklist(self):
        """Test case for delete_checklist

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}'.format(checklist_uid='checklist_uid_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_checklist_task(self):
        """Test case for delete_checklist_task

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}/task/{taskUid}'.format(checklist_uid='checklist_uid_example', task_uid='task_uid_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_template(self):
        """Test case for delete_template

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/template/{templateUid}'.format(template_uid='template_uid_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_template_task(self):
        """Test case for delete_template_task

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/template/{templateUid}/task/{taskUid}'.format(template_uid='template_uid_example', task_uid='task_uid_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_checklist(self):
        """Test case for get_checklist

        
        """
        query_string = [('client_uid', 'client_uid_example'),
                        ('secago', 789),
                        ('token', 'token_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}'.format(checklist_uid='checklist_uid_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_checklist1(self):
        """Test case for get_checklist1

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/active',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_checklist_status(self):
        """Test case for get_checklist_status

        
        """
        query_string = [('token', 'token_example'),
                        ('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}/status'.format(checklist_uid='checklist_uid_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_checklist_task(self):
        """Test case for get_checklist_task

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}/task/{taskUid}'.format(checklist_uid='checklist_uid_example', task_uid='task_uid_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_template(self):
        """Test case for get_template

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/template/{templateUid}'.format(template_uid='template_uid_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_template_task(self):
        """Test case for get_template_task

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/template/{templateUid}/task/{taskUid}'.format(template_uid='template_uid_example', task_uid='task_uid_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_template(self):
        """Test case for post_template

        
        """
        query_string = [('client_uid', 'client_uid_example'),
                        ('callsign', 'callsign_example'),
                        ('name', 'name_example'),
                        ('description', 'description_example')]
        response = self.client.open(
            '/Marti/api/excheck/template',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_mission_reference_from_checklist(self):
        """Test case for remove_mission_reference_from_checklist

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/checklist/{checklistUid}/mission/{missionName}'.format(checklist_uid='checklist_uid_example', mission_name='mission_name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_checklist(self):
        """Test case for start_checklist

        
        """
        query_string = [('client_uid', 'client_uid_example'),
                        ('callsign', 'callsign_example'),
                        ('name', 'name_example'),
                        ('description', 'description_example'),
                        ('start_time', 'start_time_example'),
                        ('default_role', 'default_role_example')]
        response = self.client.open(
            '/Marti/api/excheck/{templateUid}/start'.format(template_uid='template_uid_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_stop_checklist(self):
        """Test case for stop_checklist

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/excheck/{checklistUid}/stop'.format(checklist_uid='checklist_uid_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
