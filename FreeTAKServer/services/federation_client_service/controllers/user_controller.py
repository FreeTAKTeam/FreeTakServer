from typing import List


class UserController:
    def __init__(self) -> None:
        self.user_dict = {}

    def get_service_users(self) -> List[FederatedEvent]:
        return self.user_dict.values()

    def add_service_user(self, user: FederatedEvent) -> None:
        """ add a service user to this services user persistence mechanism

        Returns: None

        """
        self.user_dict[user.contact.uid] = user

    def remove_service_user(self, user: FederatedEvent):
        """ remove a service user from this services user persistence mechanism

        Returns: None

        """
        del self.user_dict[user.contact.uid]