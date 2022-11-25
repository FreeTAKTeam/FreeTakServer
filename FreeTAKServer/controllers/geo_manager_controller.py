from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

import pickle

config = MainConfig.instance()


class GeoManagerController:
    @staticmethod
    def update_users(users: dict) -> None:
        """update the users object"""
        with open(config.UserPersistencePath, "w") as f:
            pickle.dump(users, f)
