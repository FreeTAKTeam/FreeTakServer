from typing import Callable
from digitalpy.core.zmanager.request import Request

from FreeTAKServer.core.domain.node import Node


def serialize_to_json(message: Node, request: Request, execute_sub_action: Callable)->str:
    request.set_value("protocol", "json")
    request.set_value("message", [message])
    response = execute_sub_action("serialize")
    return response.get_value("message")[0]

def serialize_to_xml(message: Node, request: Request, execute_sub_action: Callable)->str:
    request.set_value("protocol", "xml")
    request.set_value("message", [message])
    response = execute_sub_action("serialize")
    return response.get_value("message")[0]