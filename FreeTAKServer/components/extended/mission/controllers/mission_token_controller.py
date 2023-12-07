from typing import List
from FreeTAKServer.components.extended.mission.persistence.mission import Mission
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
import jwt
import time
import uuid

from .mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()

class MissionTokenController(Controller):
    """this class is used to handle all token related operations including generating, reading, and validating
    sent tokens.
    """

    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
        ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistence_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        super().initialize(request, response)
        self.persistence_controller.initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def _load_certificate(self):
        """this method is used to load the certificate from the configuration for use in encoding and decoding the jwt.
        """
        with open(config.keyDir, "rb") as f:
            return f.read()

    def load_token(self, token_string, *args, **kwargs):
        """loads a token from a string and returns the decoded token in json format.
        """
        token = jwt.decode(token_string, self._load_certificate(), algorithms=["RS256"], options={"verify_signature": False})
        self.response.set_value("token", token)
        return self.response

    def get_token(self, mission_object: Mission, *args, **kwargs):
        """this method is used to generate a token and return it to the client in json format.
        """
        uid = str(uuid.uuid4())
        token_payload = {
            'jti': uid, 
            'iat': self._get_epoch_time(), 
            'sub': 'SUBSCRIPTION',
            'iss': '',
            'SUBSCRIPTION': uid,
            'MISSION_NAME': mission_object.name
        }

        token = jwt.encode(token_payload, self._load_certificate(), algorithm="RS256")
        self.response.set_value("token", token)
        return token

    def _get_epoch_time(self):
        """this method is used to get the current time in epoch format.
        """
        return int(time.time())