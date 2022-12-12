from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

import pickle
import copy

config = MainConfig.instance()


class GeoManagerController:
    @staticmethod
    def update_users(users: dict) -> None:
        """update the users object"""
        serialiable_users = GeoManagerController._ensure_serializable(users)
        with open(config.UserPersistencePath, "wb") as f:
            pickle.dump(serialiable_users, f)

    @staticmethod
    def _ensure_serializable(users: dict):
        serializable = {}
        for user_id, user in users.items():
            user_c = copy.deepcopy(user[1])
            if hasattr(user_c, "socket"):
                user_c.socket = None
            serializable[user_id] = user_c
        return serializable
