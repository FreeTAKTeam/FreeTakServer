"""this module contains the ClientAbstract class"""
from abc import ABC


class ClientAbstract(ABC):  # pylint: disable=too-few-public-methods
    """this is the abstract class containing the
    attributes common to all Clients"""

    conn = None
    address = tuple
    group = None
