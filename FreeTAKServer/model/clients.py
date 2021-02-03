from abc import ABC


class ClientAbstract(ABC):
    conn = None
    address = tuple
    group = None
