# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.group_name_model import GroupNameModel  # noqa: E501
from swagger_server.models.new_user_model import NewUserModel  # noqa: E501
from swagger_server.models.simple_group_with_users_model import SimpleGroupWithUsersModel  # noqa: E501
from swagger_server.models.simple_user_group_model import SimpleUserGroupModel  # noqa: E501
from swagger_server.models.user_generation_in_bulk_model import UserGenerationInBulkModel  # noqa: E501
from swagger_server.models.user_password_model import UserPasswordModel  # noqa: E501
from swagger_server.models.username_model import UsernameModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFileUserAccountManagementApiController(BaseTestCase):
    """FileUserAccountManagementApiController integration test stubs"""

    def test_change_user_password(self):
        """Test case for change_user_password

        
        """
        body = UserPasswordModel()
        response = self.client.open(
            '/user-management/api/change-user-password',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_file_users_in_bulk(self):
        """Test case for create_file_users_in_bulk

        
        """
        body = UserGenerationInBulkModel()
        response = self.client.open(
            '/user-management/api/new-users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_or_update_file_user(self):
        """Test case for create_or_update_file_user

        
        """
        body = NewUserModel()
        response = self.client.open(
            '/user-management/api/new-user',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        
        """
        response = self.client.open(
            '/user-management/api/delete-user/{username}'.format(username='username_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_group_names(self):
        """Test case for get_all_group_names

        
        """
        response = self.client.open(
            '/user-management/api/list-groupnames',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_users(self):
        """Test case for get_all_users

        
        """
        response = self.client.open(
            '/user-management/api/list-users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_groups_for_users(self):
        """Test case for get_groups_for_users

        
        """
        response = self.client.open(
            '/user-management/api/get-groups-for-user/{username}'.format(username='username_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_users_in_group(self):
        """Test case for get_users_in_group

        
        """
        response = self.client.open(
            '/user-management/api/users-in-group/{group}'.format(group='group_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_groups_for_user(self):
        """Test case for update_groups_for_user

        
        """
        body = SimpleUserGroupModel()
        response = self.client.open(
            '/user-management/api/update-groups',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
