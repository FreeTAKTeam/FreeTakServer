from digitalpy.routing.controller import Controller


class EmergencyPersistence(Controller):
    emergencies = {}

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def save_emergency(self, model_object, **kwargs) -> None:
        """this method adds a new emergency to the list of emergencies

        Args:
            emergency (Event): the new emergency model object
        """
        try:
            emergency_uid = model_object.uid
            self.emergencies[emergency_uid] = model_object
            self.request.get_value("logger").debug(
                f"added emergency: {emergency_uid} to emergencies: {self.emergencies}"
            )
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

    def get_all_emergencies(self, **kwargs) -> None:
        """this method is gets all the saved emergency objects and returns them
        as a list of emergency objects"""
        self.response.set_value("emergencies", list(self.emergencies.values()))
