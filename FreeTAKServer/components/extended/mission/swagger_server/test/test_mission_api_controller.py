# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_external_mission_data import ApiResponseExternalMissionData  # noqa: E501
from swagger_server.models.api_response_list_entry_string_string import ApiResponseListEntryStringString  # noqa: E501
from swagger_server.models.api_response_list_log_entry import ApiResponseListLogEntry  # noqa: E501
from swagger_server.models.api_response_list_mission import ApiResponseListMission  # noqa: E501
from swagger_server.models.api_response_list_mission_change import ApiResponseListMissionChange  # noqa: E501
from swagger_server.models.api_response_list_mission_invitation import ApiResponseListMissionInvitation  # noqa: E501
from swagger_server.models.api_response_list_mission_subscription import ApiResponseListMissionSubscription  # noqa: E501
from swagger_server.models.api_response_list_resource import ApiResponseListResource  # noqa: E501
from swagger_server.models.api_response_list_string import ApiResponseListString  # noqa: E501
from swagger_server.models.api_response_log_entry import ApiResponseLogEntry  # noqa: E501
from swagger_server.models.api_response_map_layer import ApiResponseMapLayer  # noqa: E501
from swagger_server.models.api_response_mission import ApiResponseMission  # noqa: E501
from swagger_server.models.api_response_mission_role import ApiResponseMissionRole  # noqa: E501
from swagger_server.models.api_response_mission_subscription import ApiResponseMissionSubscription  # noqa: E501
from swagger_server.models.api_response_navigable_set_resource import ApiResponseNavigableSetResource  # noqa: E501
from swagger_server.models.api_response_set_mission import ApiResponseSetMission  # noqa: E501
from swagger_server.models.api_response_set_mission_change import ApiResponseSetMissionChange  # noqa: E501
from swagger_server.models.api_response_set_mission_invitation import ApiResponseSetMissionInvitation  # noqa: E501
from swagger_server.models.api_response_set_string import ApiResponseSetString  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.contents_missionpackage_body import ContentsMissionpackageBody  # noqa: E501
from swagger_server.models.external_mission_data import ExternalMissionData  # noqa: E501
from swagger_server.models.log_entry import LogEntry  # noqa: E501
from swagger_server.models.map_layer import MapLayer  # noqa: E501
from swagger_server.models.mission_content import MissionContent  # noqa: E501
from swagger_server.models.mission_subscription import MissionSubscription  # noqa: E501
from swagger_server.models.missions_name_body import MissionsNameBody  # noqa: E501
from swagger_server.models.remote_subscription import RemoteSubscription  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMissionApiController(BaseTestCase):
    """MissionApiController integration test stubs"""

    def test_add_content_keyword(self):
        """Test case for add_content_keyword

        
        """
        body = ['body_example']
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/content/{hash}/keywords'.format(name='name_example', hash='hash_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_feed(self):
        """Test case for add_feed

        
        """
        query_string = [('creator_uid', 'creator_uid_example'),
                        ('data_feed_uid', 'data_feed_uid_example'),
                        ('filter_bbox', 'filter_bbox_example'),
                        ('filter_type', 'filter_type_example'),
                        ('filter_callsign', 'filter_callsign_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/feed'.format(mission_name='mission_name_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_mission_content(self):
        """Test case for add_mission_content

        
        """
        body = MissionContent()
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/contents'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_mission_package(self):
        """Test case for add_mission_package

        
        """
        body = ContentsMissionpackageBody()
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{name}/contents/missionpackage'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_uid_keyword(self):
        """Test case for add_uid_keyword

        
        """
        body = ['body_example']
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/uid/{uid}/keywords'.format(name='name_example', uid='uid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_clear_content_keywords(self):
        """Test case for clear_content_keywords

        
        """
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/content/{hash}/keywords'.format(name='name_example', hash='hash_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_clear_keywords(self):
        """Test case for clear_keywords

        
        """
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/keywords'.format(name='name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_clear_parent(self):
        """Test case for clear_parent

        
        """
        response = self.client.open(
            '/Marti/api/missions/{childName}/parent'.format(child_name='child_name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_clear_uid_keywords(self):
        """Test case for clear_uid_keywords

        
        """
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/uid/{uid}/keywords'.format(name='name_example', uid='uid_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_copy_mission(self):
        """Test case for copy_mission

        
        """
        query_string = [('creator_uid', 'creator_uid_example'),
                        ('copy_name', 'copy_name_example'),
                        ('copy_path', 'copy_path_example'),
                        ('default_role', 'default_role_example'),
                        ('password', 'password_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/copy'.format(mission_name='mission_name_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_map_layer(self):
        """Test case for create_map_layer

        
        """
        body = MapLayer()
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/maplayers'.format(mission_name='mission_name_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_mission(self):
        """Test case for create_mission

        
        """
        body = MissionsNameBody()
        query_string = [('creator_uid', ''),
                        ('group', '[\"__ANON__\"]'),
                        ('description', ''),
                        ('chat_room', ''),
                        ('base_layer', ''),
                        ('bbox', ''),
                        ('bounding_polygon', '[]'),
                        ('path', ''),
                        ('classification', ''),
                        ('tool', 'public'),
                        ('password', 'password_example'),
                        ('default_role', 'default_role_example'),
                        ('expiration', 789)]
        response = self.client.open(
            '/Marti/api/missions/{name}'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_mission_subscription(self):
        """Test case for create_mission_subscription

        
        """
        query_string = [('uid', ''),
                        ('topic', ''),
                        ('password', ''),
                        ('secago', 789),
                        ('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/subscription'.format(mission_name='mission_name_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_external_mission_data(self):
        """Test case for delete_external_mission_data

        
        """
        query_string = [('notes', 'notes_example'),
                        ('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{name}/externaldata/{id}'.format(name='name_example', id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_log_entry(self):
        """Test case for delete_log_entry

        
        """
        response = self.client.open(
            '/Marti/api/missions/logs/entries/{id}'.format(id='id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_map_layer(self):
        """Test case for delete_map_layer

        
        """
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/maplayers/{uid}'.format(mission_name='mission_name_example', uid='uid_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_mission(self):
        """Test case for delete_mission

        
        """
        query_string = [('creator_uid', ''),
                        ('deep_delete', false)]
        response = self.client.open(
            '/Marti/api/missions/{name}'.format(name='name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_mission_subscription(self):
        """Test case for delete_mission_subscription

        
        """
        query_string = [('uid', ''),
                        ('topic', ''),
                        ('disconnect_only', false)]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/subscription'.format(mission_name='mission_name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_log_entries(self):
        """Test case for get_all_log_entries

        
        """
        response = self.client.open(
            '/Marti/api/missions/all/logs',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_mission_invitations(self):
        """Test case for get_all_mission_invitations

        
        """
        query_string = [('client_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/all/invitations',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_mission_invitations_with_passwords(self):
        """Test case for get_all_mission_invitations_with_passwords

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/invitations',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_mission_subscriptions(self):
        """Test case for get_all_mission_subscriptions

        
        """
        response = self.client.open(
            '/Marti/api/missions/all/subscriptions',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_missions(self):
        """Test case for get_all_missions

        
        """
        query_string = [('password_protected', false),
                        ('default_role', false),
                        ('tool', 'public')]
        response = self.client.open(
            '/Marti/api/missions',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_children(self):
        """Test case for get_children

        
        """
        response = self.client.open(
            '/Marti/api/missions/{name}/children'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_kml(self):
        """Test case for get_kml

        
        """
        query_string = [('download', false)]
        response = self.client.open(
            '/Marti/api/missions/{name}/kml'.format(name='name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_latest_mission_cot_events(self):
        """Test case for get_latest_mission_cot_events

        
        """
        response = self.client.open(
            '/Marti/api/missions/{name}/cot'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_log_entry(self):
        """Test case for get_log_entry

        
        """
        query_string = [('secago', 789),
                        ('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/log'.format(mission_name='mission_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mission(self):
        """Test case for get_mission

        
        """
        query_string = [('password', ''),
                        ('changes', false),
                        ('logs', false),
                        ('secago', 789),
                        ('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/Marti/api/missions/{name}'.format(name='name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mission_archive(self):
        """Test case for get_mission_archive

        
        """
        response = self.client.open(
            '/Marti/api/missions/{name}/archive'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mission_changes(self):
        """Test case for get_mission_changes

        
        """
        query_string = [('secago', 789),
                        ('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00'),
                        ('squashed', true)]
        response = self.client.open(
            '/Marti/api/missions/{name}/changes'.format(name='name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mission_invitations(self):
        """Test case for get_mission_invitations

        
        """
        response = self.client.open(
            '/Marti/api/missions/{missionName}/invitations'.format(mission_name='mission_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mission_role_from_token(self):
        """Test case for get_mission_role_from_token

        
        """
        response = self.client.open(
            '/Marti/api/missions/{missionName}/role'.format(mission_name='mission_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mission_subscription_roles(self):
        """Test case for get_mission_subscription_roles

        
        """
        response = self.client.open(
            '/Marti/api/missions/{missionName}/subscriptions/roles'.format(mission_name='mission_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_mission_subscriptions(self):
        """Test case for get_mission_subscriptions

        
        """
        response = self.client.open(
            '/Marti/api/missions/{missionName}/subscriptions'.format(mission_name='mission_name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_one_log_entry(self):
        """Test case for get_one_log_entry

        
        """
        response = self.client.open(
            '/Marti/api/missions/logs/entries/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_parent(self):
        """Test case for get_parent

        
        """
        response = self.client.open(
            '/Marti/api/missions/{name}/parent'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_read_only_access_token(self):
        """Test case for get_read_only_access_token

        
        """
        query_string = [('password', '')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/token'.format(mission_name='mission_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_resource(self):
        """Test case for get_resource

        
        """
        response = self.client.open(
            '/Marti/api/resources/{hash}'.format(hash='hash_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_subscription_for_user(self):
        """Test case for get_subscription_for_user

        
        """
        query_string = [('uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/subscription'.format(mission_name='mission_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_invite_to_mission(self):
        """Test case for invite_to_mission

        
        """
        query_string = [('creator_uid', 'creator_uid_example'),
                        ('role', 'role_example')]
        response = self.client.open(
            '/Marti/api/missions/{name}/invite/{type}/{invitee}'.format(name='name_example', type='type_example', invitee='invitee_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_notify_external_data_changed(self):
        """Test case for notify_external_data_changed

        
        """
        body = 'body_example'
        query_string = [('creator_uid', 'creator_uid_example'),
                        ('notes', 'notes_example')]
        response = self.client.open(
            '/Marti/api/missions/{name}/externaldata/{id}/change'.format(name='name_example', id='id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_log_entry(self):
        """Test case for post_log_entry

        
        """
        body = LogEntry()
        response = self.client.open(
            '/Marti/api/missions/logs/entries',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_feed(self):
        """Test case for remove_feed

        
        """
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/feed/{uid}'.format(mission_name='mission_name_example', uid='uid_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_keyword(self):
        """Test case for remove_keyword

        
        """
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/keywords/{keyword}'.format(name='name_example', keyword='keyword_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_mission_content(self):
        """Test case for remove_mission_content

        
        """
        query_string = [('hash', 'hash_example'),
                        ('uid', 'uid_example'),
                        ('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/contents'.format(name='name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_password(self):
        """Test case for remove_password

        
        """
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/password'.format(name='name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_results(self):
        """Test case for results

        
        """
        response = self.client.open(
            '/Marti/api/missions/{name}/contacts'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_sync(self):
        """Test case for search_sync

        
        """
        query_string = [('box', 'box_example'),
                        ('circle', 'circle_example'),
                        ('start_time', '2013-10-20T19:20:30+01:00'),
                        ('end_time', '2013-10-20T19:20:30+01:00'),
                        ('min_altitude', 1.2),
                        ('max_altitude', 1.2),
                        ('filename', 'filename_example'),
                        ('keyword', 'keyword_example'),
                        ('mimetype', 'mimetype_example'),
                        ('name', 'name_example'),
                        ('uid', 'uid_example'),
                        ('hash', 'hash_example'),
                        ('mission', 'mission_example'),
                        ('tool', 'tool_example')]
        response = self.client.open(
            '/Marti/api/sync/search',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_mission_archive(self):
        """Test case for send_mission_archive

        
        """
        response = self.client.open(
            '/Marti/api/missions/{name}/send'.format(name='name_example'),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_mission_invites(self):
        """Test case for send_mission_invites

        
        """
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{name}/invite'.format(name='name_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_expiration1(self):
        """Test case for set_expiration1

        
        """
        query_string = [('expiration', 789)]
        response = self.client.open(
            '/Marti/api/missions/{name}/expiration'.format(name='name_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_external_mission_data(self):
        """Test case for set_external_mission_data

        
        """
        body = ExternalMissionData()
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{name}/externaldata'.format(name='name_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_keywords(self):
        """Test case for set_keywords

        
        """
        body = ['body_example']
        query_string = [('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/keywords'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_mission_role(self):
        """Test case for set_mission_role

        
        """
        query_string = [('client_uid', ''),
                        ('username', ''),
                        ('role', 'role_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/role'.format(mission_name='mission_name_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_parent(self):
        """Test case for set_parent

        
        """
        response = self.client.open(
            '/Marti/api/missions/{childName}/parent/{parentName}'.format(child_name='child_name_example', parent_name='parent_name_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_password(self):
        """Test case for set_password

        
        """
        query_string = [('password', ''),
                        ('creator_uid', '')]
        response = self.client.open(
            '/Marti/api/missions/{name}/password'.format(name='name_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_subscription_role(self):
        """Test case for set_subscription_role

        
        """
        body = [MissionSubscription()]
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/subscription'.format(mission_name='mission_name_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_uninvite_from_mission(self):
        """Test case for uninvite_from_mission

        
        """
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{name}/invite/{type}/{invitee}'.format(name='name_example', type='type_example', invitee='invitee_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_log_entry(self):
        """Test case for update_log_entry

        
        """
        body = LogEntry()
        response = self.client.open(
            '/Marti/api/missions/logs/entries',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_map_layer(self):
        """Test case for update_map_layer

        
        """
        body = MapLayer()
        query_string = [('creator_uid', 'creator_uid_example')]
        response = self.client.open(
            '/Marti/api/missions/{missionName}/maplayers'.format(mission_name='mission_name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
