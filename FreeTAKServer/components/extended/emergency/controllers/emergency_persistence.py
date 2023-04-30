"""this file contains the emergency component's persistency layer"""
import codecs
from ..configuration.emergency_constants import PERSISTENCE_PATH
from digitalpy.core.main.controller import Controller
import json
import os
import pickle


class EmergencyPersistence(Controller):
    """this class is responsible for managing saved emergencies"""

    def __init__(self, request, response, action_mapper, configuration):
        super().__init__(
            request=request,
            response=response,
            action_mapper=action_mapper,
            configuration=configuration,
        )
        self._persistence = {
            "emergencies": {},
        }

        # create the mapping persistence if it doesn't exist already
        if not os.path.exists(PERSISTENCE_PATH):
            with open(PERSISTENCE_PATH, mode="w+", encoding="utf-8") as f:
                json.dump(self._persistence, f)

        # load the mapping persistence into memory
        with open(PERSISTENCE_PATH, mode="r+", encoding="utf-8") as f:
            self._persistence = json.load(f)
            self.emergencies = self._persistence["emergencies"]

        super().__init__(request, response, action_mapper, configuration)
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def save_emergency(self, model_object, **kwargs) -> None:
        """this method adds a new emergency to the list of emergencies

        Args:
            model_object (Event): the new emergency model object
        """
        try:
            emergency_uid = model_object.uid
            self.emergencies[emergency_uid] = codecs.encode(
                pickle.dumps(model_object), "base64"
            ).decode()

            self.request.get_value("logger").debug(
                f"added emergency: {emergency_uid} to emergencies: {self.emergencies}"
            )
            self._update_persistence()
        except Exception as error:
            self.request.get_value("logger").error(
                f"error adding emergency to emergencies {error}"
            )

    def delete_emergency(self, model_object, **kwargs) -> None:
        """this method removes the specified emergency from the list of emergencies

        Args:
            emergency (Event): the emergency delete model object
        """
        del self.emergencies[model_object.uid]
        self._update_persistence()

    def get_all_emergencies(self, **kwargs) -> None:
        """this method is gets all the saved emergency objects and returns them
        as a list of emergency objects"""
        self._sync_persistence()
        emergencies = [
            pickle.loads(codecs.decode(emergency.encode(), "base-64"))
            for emergency in self.emergencies.values()
        ]
        self.response.set_value("emergencies", list(emergencies))

    def _sync_persistence(self):
        """synchronize the current, in-memory state, with the persistence"""
        with open(PERSISTENCE_PATH, mode="r", encoding="utf-8") as f:
            self._persistence = json.load(f)

    def _update_persistence(self):
        """update the persistence with the in memory state"""
        # TODO: this form of persistence runs the risk of causing deletions
        # if it is being written to at the same time, to avoid this we
        # should be using a real database or at least a recognized
        # (preferably ACID) persistence mechanism
        with open(PERSISTENCE_PATH, mode="w", encoding="utf-8") as f:
            json.dump(self._persistence, f)
