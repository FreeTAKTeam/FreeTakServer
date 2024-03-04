from types import ModuleType
from typing import Any, List, Optional, Type
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.parsing.load_configuration import ModelConfiguration
from digitalpy.core.domain.node import Node
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
import uuid

from .. import domain


class Domain(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        domain_action_mapper: ActionMapper,
        configuration: Configuration,
        **kwargs,
    ):
        super().__init__(request, response, domain_action_mapper, configuration)
        self.domain = domain

    def execute(self, method=None):
        return getattr(self, method)(**self.request.get_values())

    def add_child(self, node: Node, child: Node, **kwargs) -> None:
        """add a child to a node

        Args:
            node (Node): the origin node
            child (Node): the node to be added as the original node

        Returns:
            _type_: _description_
        """
        return node.add_child(child)

    def create_node(self, configuration: ModelConfiguration, object_class_name: str, id:str=None, **kwargs) -> Node:
        """this method creates a new node object

        Args:
            configuration (Configuration): _description_
            object_class_name (str): _description_
            id (str): the id of the created node
        """
        if id is None:
            id = str(uuid.uuid1())
        # allow the domain to be extended
        domaindict = self._extend_domain(self.domain, kwargs.get('extended_domain', {}))
        # retrieve the original object class
        object_class = domaindict[object_class_name]
        # instantiate an oid for the instance
        oid = ObjectFactory.get_instance("ObjectId", {"id": id, "type": object_class_name})
        # instantiate the object class
        object_class_instance = object_class(configuration, domaindict, oid=oid)
        # set the module object
        self.response.set_value("model_object", object_class_instance)
        return object_class_instance

    def _extend_domain(self, domain: ModuleType, extended_domain: dict) -> dict:
        """this method is responsible for adding domain extensions from a given component

        Args:
            domain (_type_): the base domain package
            extended_domain (_type_): the updated domain package

        Returns:
            ModuleType: an updated domain
        """
        domaindict = domain.__dict__.copy()
        for key, value in extended_domain.items():
            domaindict[key] = value
        return domaindict

    def delete_child(self, node: Node, child_id: str, **kwargs):
        """delete a child node

        Args:
            node (Node): the node from which to remove the child
            child_id (str): the id of the child to be deleted

        Returns:
            None
        """
        return node.delete_child(child_id)

    def get_children_ex(
        self,
        id,
        node: Node,
        children_type,
        values,
        properties,
        use_regex=True,
        **kwargs,
    ):
        self.response.set_value(
            "children",
            node.get_children_ex(
                id, node, children_type, values, properties, use_regex
            ),
        )

def get_first_child(self, node: Node, child_type: Type[Node], values: "dict[str, Any]", properties: "dict[str, Any]", use_regex: bool = True, **kwargs) -> Optional[Node]:
    """Returns the first child of the given node that matches the given child type, values, and properties.
    
    Args:
        node (Node): The node to get the first child of.
        child_type (Type[Node]): The type of the child to find.
        values (dict[str, Any]): The values the child must have.
        properties (dict[str, Any]): The properties the child must have.
        use_regex (bool, optional): Whether to use regular expressions to match values and properties. Defaults to True.
        **kwargs: Additional keyword arguments.
    
    Returns:
        Optional[Node]: The first child that matches the given child type, values, and properties, or None if no such child is found.
    """
    self.response.set_value("first_child", node.get_first_child(child_type, values, properties, use_regex))

def get_next_sibling(self, node: Node, **kwargs) -> Optional[Node]:
    """Returns the next sibling of the given node.
    
    Args:
        node (Node): The node to get the next sibling of.
        **kwargs: Additional keyword arguments.
    
    Returns:
        Optional[Node]: The next sibling of the given node, or None if the node has no next sibling.
    """
    self.response.set_value("next_sibling", node.get_next_sibling())

def get_num_children(self, node: Node, children_type: Optional[Type[Node]] = None, **kwargs) -> int:
    """Returns the number of children the given node has.
    
    Args:
        node (Node): The node to get the number of children of.
        children_type (Optional[Type[Node]], optional): The type of children to count. If not specified, all children are counted. Defaults to None.
        **kwargs: Additional keyword arguments.
    
    Returns:
        int: The number of children the given node has.
    """
    self.response.set_value("num_children", node.get_num_children(children_type))

def get_num_parents(self, node: Node, parent_types: Optional[List[Type[Node]]] = None, **kwargs) -> int:
    """Returns the number of parents the given node has.
    
    Args:
        node (Node): The node to get the number of parents of.
        parent_types (Optional[List[Type[Node]]], optional): The types of parents to count. If not specified, all parents are counted. Defaults to None.
        **kwargs: Additional keyword arguments.
    
    Returns:
        int: The number of parents the given node has.
    """
    self.response.set_value("num_parents", node.get_num_parents(parent_types))
    
def get_previous_sibling(self, node: Node) -> Optional[Node]:
    """Returns the previous sibling of the given node.

    Args:
        node (Node): The node to get the previous sibling of.

    Returns:
        Optional[Node]: The previous sibling of the given node, or None if the node has no previous sibling.
    """
    self.response.set_value("previous_sibling", node.get_previous_sibling())

def get_parent(self, node: Node) -> Optional[Node]:
    """Returns the parent of the given node.

    Args:
        node (Node): The node to get the parent of.

    Returns:
        Optional[Node]: The parent of the given node, or None if the node has no parent.
    """
    self.response.set_value("parent", node.get_parent())
