import uuid
import re
from typing import Dict, Any
from digitalpy.core.persistence.impl.default_persistent_object import DefaultPersistentObject
from digitalpy.core.parsing.load_configuration import Configuration
from digitalpy.core.domain.object_id import ObjectId
from digitalpy.core.persistence.persistent_object import PersistentObject
from digitalpy.core.persistence.persistent_object_proxy import PersistentObjectProxy
from digitalpy.core.persistence.build_depth import BuildDepth


class Node(DefaultPersistentObject):
    """Node adds the concept of relations to PersistentObject. It is the basic
    component for building object trees (although a Node can have more than one
    parents). Relations are stored as values where the value name is the role name.
    The Node class implements the _Composite Pattern_. Use the methods add_node(),
    delete_node() to build/modify trees.
    """

    __addedNodes = []
    __deletedNodes = []
    __logger = None
    __orderedNodes = None
    __parentGetValueMethod = None
    RELATION_STATE_INITIALIZED = -3
    RELATION_STATE_INITIALIZING = -2
    RELATION_STATE_LOADED = -4
    RELATION_STATE_UNINITIALIZED = -1
    __relationStates = []

    def __init__(
        self,
        node_type,
        configuration: Configuration,
        model,
        oid: ObjectId = None,
        initial_data=None,
    ) -> None:
        super().__init__(oid, initial_data)
        self._children: Dict[str, Node] = {}
        self._parents: Dict[str, Node] = {}
        self._depth = -1
        self._path = ""
        self._relationship_definition = configuration.elements[self.__class__.__name__]
        self._add_relationships(configuration, model)

    def _add_relationships(self, configuration: Configuration, model) -> None:
        for (
            relationship_name,
            relationship_def,
        ) in self._relationship_definition.relationships.items():
            child_class = getattr(model, relationship_name)
            child_instance = child_class(configuration, model)
            self.add_child(child_instance)

    def get_first_child(self, child_type, values, properties, use_regex=True):
        """Get the first child that matches given conditions."""
        children = self.get_children_ex(
            None,
            children_type=child_type,
            values=values,
            properties=properties,
            use_regex=use_regex,
        )
        if len(children) > 0:
            return children[0]
        else:
            return None

    def get_children(self):
        """Get the Node's children."""
        return self._children
        # return self.get_relatives('child')

    def get_relatives(self, hirearchy_type):
        relatives = []
        relations = self.get_relations(hirearchy_type)
        for relation in relations:
            cur_relatives = super().get_value(relation.get_other_role())
            if cur_relatives is None:
                continue
            if not isinstance(cur_relatives, list):
                cur_relatives = [cur_relatives]
            for cur_relative in cur_relatives:
                if isinstance(cur_relatives, PersistentObjectProxy):
                    continue
                else:
                    relatives.append(cur_relative)

    def get_children_ex(
        self,
        oid=None,
        role=None,
        children_type=None,
        values=None,
        properties=None,
        use_regex=True,
    ):
        """Get the children that match given conditions."""
        if role is not None:
            child_roles = self.get_possible_children()
            if child_roles[role]:
                raise Exception("No child role defined with name %s" % role)
            nodes = super().get_value(role)
            if not isinstance(nodes, list):
                nodes = [nodes]
            children = []
            for cur_node in nodes:
                if isinstance(cur_node, PersistentObject):
                    children = cur_node
            return self.filter(
                children, oid, children_type, values, properties, use_regex
            )
        else:
            return self.filter(
                self.get_children(), oid, children_type, values, properties, use_regex
            )

    def get_possible_children(self):
        result = []
        relations = self.get_relations("child")
        for cur_relation in relations:
            result[cur_relation.get_other_role()] = cur_relation
        return result

    def get_num_children(self, children_type=None):
        count = 0
        if children_type:
            for child in self._children.values():
                if child.get_type() == children_type:
                    count += 1
            return count
        else:
            return len(self._children)

    def add_child(self, child):
        if self.validate_child_addition(child):
            self._children[child.get_id()] = child
            setattr(self, child.__class__.__name__, child)
            child.set_parent(self)
        else:
            raise TypeError("child must be an instance of Node")

    def validate_child_addition(self, child):
        if isinstance(child, Node):
            child_type = child.get_type()
            if child_type in self._relationship_definition.relationships:
                relationship_requirements = self._relationship_definition.relationships[
                    child_type
                ]
                children = self.get_children_ex(children_type=child_type)
                if relationship_requirements["max_occurs"] == len(children):
                    return False
            return True
        raise TypeError("children must inherit from type Node")

    def delete_child(self, child_id):
        del self._children[child_id]

    def validate_child_removal(self, child):
        if isinstance(child, Node):
            child_type = child.get_type()
            if child_type in self._relationship_definition:
                relationship_requirements = self._relationship_definition[child_type]
                if relationship_requirements["aggregation"] == "composite":
                    return False
                children = self.get_children_ex(children_type=child_type)
                if relationship_requirements["min_occurs"] == len(children):
                    return False
            return True
        raise TypeError("children must inherit from type Node")

    def update_parent(self, parent, recursive=True):
        if parent in self._parents:
            return None
        else:
            self._parents[parent.get_id()] = parent

    def filter(self, node_list, oid, node_type, values, properties, use_regex):
        """Get Nodes that match given conditions from a list."""
        return_array = []
        for key, node in node_list.items():
            if isinstance(node, PersistentObject):
                match = True
                # check id
                if oid != None and node.get_oid() != oid:
                    match = False
                # check type
                if node_type != None and node.get_type() != node_type:
                    match = False
                # check properties
                if properties != None and isinstance(properties, dict):
                    for key, value in properties.items():
                        node_property = node.get_property(key)
                        if use_regex and not re.match(
                            "/" + value + "/m", node_property
                        ):
                            match = False
                            break

                        elif not hasattr(node, key) and not use_regex:
                            match = False
                            break

                # check values
                if values != None and isinstance(values, dict):
                    for key, value in properties.items():
                        node_value = self.get_value(key)
                        if use_regex and not re.match("/" + value + "/m", node_value):
                            match = False
                            break
                if match:
                    return_array.append(node)
        return return_array

    def get_next_sibling(self):
        parent = self.get_parent()
        if parent is not None:
            parent_children = parent.get_children()
            next_sibling = None

            for index, child in enumerate(parent_children):
                if child.get_oid() == self._oid and index < len(parent_children) - 1:
                    next_sibling = parent_children[index + 1]
                    break

            if next_sibling is not None:
                return next_sibling

            return None

    def get_previous_sibling(self):
        parent = self.get_parent()
        if parent is not None:
            parent_children = parent.get_children()
            previous_sibling = None
            for index, child in enumerate(parent_children):
                if parent.get_oid() == self._oid and index > 0:
                    previous_sibling = parent_children[index - 1]
                    break
            if previous_sibling is not None:
                return previous_sibling
            return None

    def get_num_parents(self, parent_type=None):
        """Get the number of parents of the Node."""
        count = 0

        if parent_type is not None:
            for index, parent in enumerate(self._parents):
                if parent.get_type() == parent_type:
                    count += 1

        else:
            count = len(self._parents)

        return count

    def set_parent(self, parent):
        """Set the parent of the Node"""
        if isinstance(parent, Node):
            self._parents[str(parent.get_oid())] = parent

    def get_first_parent(
        self,
        role: Any = None,
        type: Any = None,
        values: Any = None,
        properties: Any = None,
        use_regex: Any = True,
    ):
        """Get the first super() that matches given conditions.
           @param role The role that the super() should match (optional, default:
        _None_).
           @param type The type that the super() should match (either fully qualified
        or simple, if not ambiguous) (optional, default: _None_).
           @param values An associative array holding key value pairs that the super()
        values should match (optional, default: _None_).
           @param properties An associative array holding key value pairs that the
        super() properties should match (optional, default: _None_).
           @param use_reg_exp Boolean whether to interpret the given values/properties
        as regular expressions or not (default: _True_)
           @return Node instance or None.
        """
        parents = self.get_parents_ex(None, role, type, values, properties, use_regex)
        if len(parents) > 0:
            return parents[0]

        else:
            return None

    def get_parents(self):
        """Get the Nodes parents."""
        return self._parents

    def get_parents_ex(self, oid, type, values, properties, use_regex=True):
        """Get the parents that match given conditions."""
        return self.filter(self._parents, oid, type, values, properties, use_regex)

    def get_depth(self):
        self._depth = 0
        parent = self.get_parent()
        while parent is not None and isinstance(parent, Node):
            self._depth += 1
            parent = parent.get_parent()
        return self._depth

    def __clone() -> Any:
        NotImplementedError("this method has not yet been implemented")

    def accept_visitor(self, visitor: Any) -> Any:
        """Accept a Visitor. For use with the _Visitor Pattern_."""
        visitor.visit(self)

    def add_node(
        self,
        other: PersistentObject,
        role: Any = None,
        force_set: bool = False,
        track_change: bool = True,
        update_other_side: bool = True,
    ) -> Any:
        """Add a Node to the given relation. Delegates to set_value internally."""
        mapper = self.get_mapper()
        if role == None:
            other_type = other.get_type()
            relations = mapper.get_relations_by_type(other_type)
            if len(relations) > 0:
                role = relations[0].get_other_role()
            else:
                role = other_type
        # get the relation description
        rel_desc = mapper.get_relation(role)

        value = other
        old_value = super().get_value(role)
        added_nodes = []  # this array contains the other node or nothing
        if not rel_desc or rel_desc.is_multi_valued():
            # check multiplicity if multivalued
            max_multiplicity = rel_desc.get_other_max_multiplicity()
            if (
                rel_desc.is_multi_valued()
                and not (max_multiplicity == "unbounded")
                and len(old_value) >= max_multiplicity
            ):
                raise ValueError(
                    "Maximum number of related objects exceeded: "
                    + role
                    + " ("
                    + (len(old_value) + 1)
                    + " > "
                    + max_multiplicity
                    + ")"
                )

            # make sure that the value is an array if multivalued
            merge_result = self.merge_object_lists(old_value, [value])
            value = merge_result["result"]
            added_nodes = merge_result["added"]

        elif (
            old_value == None
            and value != None
            or old_value.get_oid().__toString() != value.get_oid().__toString()
        ):
            added_nodes.append(value)

        result_1 = len(added_nodes) > 0 and super().set_value(
            role, value, force_set, track_change
        )

        # remember the addition
        if len(added_nodes) > 0:
            if not role in self.added_nodes:
                self.added_nodes[role] = []

        self.added_nodes[role].append(other)

        # propagate add action to the other object
        result_2 = True
        if update_other_side:

            if rel_desc:
                this_role = rel_desc.get_this_role()
            else:
                None

            result_2 = other.add_node(self, this_role, force_set, track_change, False)

        return result_1 & result_2

    def add_relation(self, name: Any) -> Any:
        """Add an uninitialized relation. The relation will be initialized (proxies for
        related objects will be added) on first access.
           @param name The relation name (= role)
        """
        if not self.has_value(name):
            self.relation_states[name] = Node.RELATION_STATE_UNINITIALIZED
            self.set_value_internal(name, None)

    def delete_node(self, other: PersistentObject, role: Any = None, update_other_side: Any = True) -> bool:
        """Delete a Node from the given relation."""
        mapper = self.get_Mapper()

        # set role if missing
        if role is None:
            other_Type = other.get_type()
            relations = mapper.get_relations_by_type(other_Type)
            if relations:
                role = relations[0].get_other_role()
            else:
                role = other_Type

        nodes = self.get_value(role)
        if not nodes:
            # nothing to delete
            return False

        # get the relation description
        rel_desc = mapper.get_relation(role)

        oid = other.get_O_I_D()
        if isinstance(nodes, list):
            # multi valued relation
            for i, node in enumerate(nodes):
                if node.get_oid() == oid:
                    # remove child
                    nodes.pop(i)
                    break
        else:
            # single valued relation
            if nodes.get_oid() == oid:
                # remove child
                nodes = None

        super().set_value(role, nodes)

        # remember the deletion
        self.deleted_Nodes.setdefault(role, []).append(other.get_oid())
        self.set_State(PersistentObject.STATE_DIRTY)

        # propagate add action to the other object
        if update_other_side:
            if rel_desc:
                this_role = rel_desc.get_This_Role()
            else:
                this_role = None
            other.delete_node(self, this_role, False)
        return True

    def filter(
        node_list: list,
        oid: ObjectId = None,
        node_type: Any = None,
        values: Any = None,
        properties: Any = None,
        use_regex: Any = True,
    ) -> Any:
        """Get Nodes that match given conditions from a list.
           @param node_list An array of nodes to filter or a single Node.
           @param oid The object id that the Nodes should match (optional, default:
        _None_)
           @param type The type that the Nodes should match (either fully qualified or
        simple, if not ambiguous) (optional, default: _None_)
           @param values An associative array holding key value pairs that the Node
        values should match (values are interpreted as regular expression, optional,
        default: _None_)
           @param properties An associative array holding key value pairs that the
        Node properties should match (values are interpreted as regular expression,
        optional, default: _None_)
           @param use_reg_exp Boolean whether to interpret the given values/properties
        as regular expressions or not (default: _True_)
           @return An Array holding references to the Nodes that matched.
        """
        return_array = []
        for key, node in node_list.items():
            if isinstance(node, PersistentObject):
                match = True
                # check id
                if oid != None and node.get_oid() != oid:
                    match = False
                # check type
                if node_type != None and node.get_type() != node_type:
                    match = False
                # check properties
                if properties != None and isinstance(properties, dict):
                    for key, value in properties.items():
                        node_property = node.get_property(key)
                        if use_regex and not re.match(
                            "/" + value + "/m", node_property
                        ):
                            match = False
                            break

                        elif not hasattr(node, key) and not use_regex:
                            match = False
                            break

                # check values
                if values != None and isinstance(values, dict):
                    for key, value in properties.items():
                        node_value = self.get_value(key)
                        if use_regex and not re.match("/" + value + "/m", node_value):
                            match = False
                            break
                if match:
                    return_array.append(node)
        return return_array

    def get_added_nodes(self) -> Any:
        """Get the object ids of the nodes that were added since the node was loaded.
        Persistence mappers use this method when persisting the node relations.
           @return Associative array with the roles as keys and an array of
        PersistentObject instances as values
        """
        return self.added_nodes

    def get_children(self, mem_only: bool = True) -> Any:
        """Get the Node's children.
           @param mem_only Boolean whether to only get the loaded children or all
        children (default: _True_).
           @return Array PersistentObject instances.
        """
        return self.get_relatives("child", mem_only)

    def get_children_ex(
        self,
        oid: ObjectId = None,
        role: Any = None,
        type: Any = None,
        values: Any = None,
        properties: Any = None,
        use_reg_exp: Any = True,
    ) -> Any:
        """Get the children that match given conditions.
           @note This method will only return objects that are already loaded, to get
        all objects in the given relation (including proxies), use the Node.get_value()
        method and filter the returned list afterwards.
           @param oid The object id that the children should match (optional, default:
        _None_).
           @param role The role that the children should match (optional, default:
        _None_).
           @param type The type that the children should match (either fully qualified
        or simple, if not ambiguous) (optional, default: _None_).
           @param values An associative array holding key value pairs that the
        children values should match (optional, default: _None_).
           @param properties An associative array holding key value pairs that the
        children properties should match (optional, default: _None_).
           @param use_reg_exp Boolean whether to interpret the given values/properties
        as regular expressions or not (default: _True_)
           @return Array containing children Nodes that matched (proxies not included).
        """
        if role != None:
            # nodes of a given role are requested
            # make sure it is a child role
            child_Roles = self.get_possible_children()
            if not role in child_Roles:
                raise ValueError("_No child role defined with name: " + role)

            # we are only looking for nodes that are in memory already
            nodes = super().get_value(role)
            if not isinstance(nodes, list):
                nodes = [nodes]

            # sort out proxies
            children = []
            for node in nodes:
                if isinstance(node, PersistentObject):
                    children.append(node)

            return self.filter(children, oid, type, values, properties, use_reg_exp)

        else:
            return self.filter(
                self.get_children(), oid, type, values, properties, use_reg_exp
            )

    def get_deleted_nodes(self) -> Any:
        """Get the object ids of the nodes that were deleted since the node was loaded.
        Persistence mappers use this method when persisting the node relations.
           @return Associative array with the roles as keys and an array of ObjectId
        instances as values
        """
        return self.deleted_nodes

    def get_indispensable_objects(self) -> Any:
        """@see PersistentObject.get_indispensable_objects()"""
        return self.get_parents()

    def get_node_order(self) -> Any:
        """Get the order of related Node instances, if it was defined using the Node.
        set_node_order() method.
           @return Associative array of with keys 'ordered', 'moved', 'role' or None
        """
        return self.ordered_nodes

    def get_node_relation(self, object_instance: Any) -> Any:
        """Get the relation description for a given node.
        @param object PersistentObject instance to look for
        @return RelationDescription instance or None, if the Node is not related
        """
        relations = self.get_Relations()
        for relation in relations:
            relatives = super().get_value(relation.get_Other_Role())
            if (
                isinstance(relatives, Node)
                and relatives.get_oid() == object_instance.get_oid()
            ):
                return relation

            elif isinstance(relatives, list):
                for relative in relatives:
                    if relative.get_oid() == object_instance.get_oid():
                        return relation

        return None

    def get_num_children(self, mem_only: Any = True) -> Any:
        """Get the number of children of the Node.
           @param mem_only Boolean whether to only get the number of loaded children or
        all children (default: _True_).
           @return The number of children.
        """
        return self.get_num_relatives("child", mem_only)

    def get_num_parents(self, mem_only: Any = True) -> Any:
        """Get the number of parents of the Node.
           @param mem_only Boolean whether to only get the number of loaded parents or
        all parents (default: _True_).
           @return The number of parents.
        """
        return self.get_num_relatives("parent", mem_only)

    def get_num_relatives(self, hierarchy_type: Any, mem_only: Any = True) -> Any:
        """Get the number of relatives of a given hierarchy_type.
           @param hierarchy_type @see PersistenceMapper.get_relations
           @param mem_only Boolean whether to only get the number of the relatives in
        memory or all relatives (default: _True_).
           @return The number of relatives.
        """
        return len(self.get_relatives(hierarchy_type, mem_only))

    def get_parent(self) -> Any:
        """Get the Node's super(). This method exists for compatibility with previous
        versions. It returns the first super().
           @return Node
        """
        if len(self._parents) > 0:
            return list(self._parents.values())[0]
        else:
            return None

    def get_parents(self, mem_only: Any = True) -> Any:
        """Get the Nodes parents.
           @param mem_only Boolean whether to only get the loaded parents or all
        parents (default: _True_).
           @return Array PersistentObject instances.
        """
        return self.get_relatives("parent", mem_only)

    def get_parents_ex(
        self,
        oid: ObjectId = None,
        role: Any = None,
        type: Any = None,
        values: Any = None,
        properties: Any = None,
        use_reg_exp: Any = True,
    ) -> Any:
        """Get the parents that match given conditions.
           @note This method will only return objects that are already loaded, to get
        all objects in the given relation (including proxies), use the Node.get_value()
        method and filter the returned list afterwards.
           @param oid The object id that the super() should match (optional, default:
        _None_).
           @param role The role that the parents should match (optional, default:
        _None_).
           @param type The type that the parents should match (either fully qualified
        or simple, if not ambiguous) (optional, default: _None_).
           @param values An associative array holding key value pairs that the super()
        values should match (optional, default: _None_).
           @param properties An associative array holding key value pairs that the
        super() properties should match (optional, default: _None_).
           @param use_reg_exp Boolean whether to interpret the given values/properties
        as regular expressions or not (default: _True_)
           @return Array containing super() Nodes that matched (proxies not included).
        """
        if role != None:
            # nodes of a given role are requested
            # make sure it is a parent role
            parent_roles = self.get_possible_parents()
            if not role in parent_roles:
                raise ValueError("_No parent role defined with name: " + role)

            # we are only looking for nodes that are in memory already
            nodes = super().get_Value(role)
            if not isinstance(nodes, list):
                nodes = [nodes]

            # sort out proxies
            parents = []
            for node in nodes:
                if isinstance(node, PersistentObject):
                    parents.append(node)

            return self.filter(parents, oid, type, values, properties, use_reg_exp)

        else:
            return self.filter(
                self.get_Parents(), oid, type, values, properties, use_reg_exp
            )

    def get_possible_children(self) -> Any:
        """Get possible children of this node type (independent of existing children).
           @return An Array with role names as keys and RelationDescription instances
        as values.
        """
        result = []
        relations = self.get_relations("child")
        for cur_relation in relations:
            result[cur_relation.get_other_role()] = cur_relation

        return result

    def get_possible_parents(self) -> Any:
        """Get possible parents of this node type (independent of existing parents).
           @return An Array with role names as keys and RelationDescription instances
        as values.
        """
        result = []
        relations = self.get_relations("parent")
        for cur_relation in relations:
            result[cur_relation.get_other_role()] = cur_relation

        return result

    def get_relation_names(self) -> Any:
        """Get the names of all relations.
        @return An array of relation names.
        """
        result = []
        relations = self.get_relations()
        for cur_relation in relations:
            result.append(cur_relation.get_other_role())

        return result

    def get_relations(self, hierarchy_type: Any = "all") -> Any:
        """Get the relation descriptions of a given hierarchy_type.
        @param hierarchy_type @see PersistenceMapper.get_relations (default: 'all')
        @return An array containing the RelationDescription instances.
        """
        return self.get_mapper().get_relations(hierarchy_type)

    def get_relatives(self, hierarchy_type: Any, mem_only: Any = True) -> Any:
        """Get the relatives of a given hierarchy_type.
           @param hierarchy_type @see PersistenceMapper.get_relations
           @param mem_only Boolean whether to only get the relatives in memory or all
        relatives (including proxies) (default: _True_).
           @return An array containing the relatives.
        """
        relatives = []
        relations = self.get_relations(hierarchy_type)
        for cur_relation in relations:
            cur_relatives = None
            if mem_only:
                cur_relatives = super().get_value(cur_relation.get_other_role())

            else:
                cur_relatives = self.get_value(cur_relation.get_other_role())

            if not cur_relatives:
                continue

            if not isinstance(cur_relatives, list):
                cur_relatives = [cur_relatives]

            for cur_relative in cur_relatives:
                if isinstance(cur_relative, PersistentObjectProxy) and mem_only:
                    # ignore proxies
                    continue

                else:
                    relatives.append(cur_relative)

        return relatives

    def get_value(self, name: Any) -> Any:
        # initialize a relation value, if not done before
        value = super().get_value(name)
        if (name in self.relation_states) and self.relation_states[
            name
        ] == self.RELATION_STATE_UNINITIALIZED:

            self.relation_states[name] = self.RELATION_STATE_INITIALIZING
            mapper = self.get_mapper()
            all_relatives = mapper.load_relation([self], name, BuildDepth.PROXIES_ONLY)
            oid_str = str(self.get_oid())
            if oid_str in all_relatives:
                relatives = all_relatives[oid_str]
            else:
                relatives = None

            rel_desc = mapper.get_relation(name)
            if rel_desc.is_multi_valued():
                merge_result = self.merge_object_lists(value, relatives)
                value = merge_result["result"]

            else:
                if relatives is not None:
                    value = relatives[0]
                else:
                    value = None

            self.set_value_internal(name, value)
            self.relation_states[name] = self.RELATION_STATE_INITIALIZED

        return value

    def get_value_names(self, exclude_transient: Any = False) -> Any:
        # exclude relations
        all_attributes = super().get_value_names(exclude_transient)
        attributes = []
        mapper = self.get_mapper()
        for attribute in all_attributes:
            if not mapper.has_relation(attribute):
                attributes.append(attribute)

        return attributes

    def load_children(
        self, role: Any = None, build_depth: Any = BuildDepth.SINGLE
    ) -> Any:
        """Load the children of a given role and add them. If all children should be
        loaded, set the role parameter to None.
           @param role The role of children to load (maybe None, to load all children)
        (default: _None_)
           @param build_depth One of the BUILDDEPTH constants or a number describing
        the number of generations to build (default: _BuildDepth.SINGLE_)
        """
        if role != None:
            self.load_relations([role], build_depth)

        else:
            self.load_relations(self.get_possible_children().keys(), build_depth)

    def load_parents(
        self, role: Any = None, build_depth: Any = BuildDepth.SINGLE
    ) -> Any:
        """Load the parents of a given role and add them. If all parents should be loaded,
        set the role parameter to None.
           @param role The role of parents to load (maybe None, to load all parents)
        (default: _None_)
           @param build_depth One of the BUILDDEPTH constants or a number describing
        the number of generations to build (default: _BuildDepth.SINGLE_)
        """
        if role != None:
            self.load_relations([role], build_depth)

        else:
            self.load_relations(self.get_possible_parents().keys(), build_depth)

    def load_relations(self, roles: list, build_depth: Any = BuildDepth.SINGLE) -> Any:
        """Load all objects in the given set of relations"""
        old_state = self.get_state()
        for cur_role in roles:
            if (cur_role in self.relation_states) and self.relation_states[
                cur_role
            ] != self.RELATION_STATE_LOADED:
                relatives = []

                # resolve proxies if the relation is already initialized
                if self.relation_states[cur_role] == self.RELATION_STATE_INITIALIZED:
                    proxies = self.get_value(cur_role)
                    if (isinstance(proxies), list):
                        for cur_relative in proxies:
                            if isinstance(cur_relative, PersistentObjectProxy):
                                # resolve proxies
                                cur_relative.resolve(build_depth)
                                relatives.append(cur_relative.get_real_subject())

                            else:
                                relatives.append(cur_relative)

                # otherwise load the objects directly
                else:
                    mapper = self.get_mapper()
                    all_relatives = mapper.load_relation([self], cur_role, build_depth)
                    oid_str = self.get_o_i_d().__toString()
                    if oid_str in all_relatives:
                        relatives = all_relatives[oid_str]
                    else:
                        relatives = None
                    rel_desc = mapper.get_relation(cur_role)
                    if not rel_desc.is_multi_valued():
                        if relatives is not None:
                            relatives = relatives[0]
                        else:
                            relatives = None

                self.set_value_internal(cur_role, relatives)
                self.relation_states[cur_role] = self.RELATION_STATE_LOADED

        self.set_state(old_state)

    @staticmethod
    def merge_object_lists(list_1: Any, list_2: Any) -> Any:
        """Merge two object lists using the following rules: - proxies in list_1 are
        replaced by the appropriate objects from list_2 - proxies/objects from list_2
        that don't exist in list_1 are added to list_1
           @param list_1 Array of PersistentObject(Proxy) instances
           @param list_2 Array of PersistentObject(Proxy) instances
           @return Associative array with keys 'result' and 'added' and arrays of all
        and only added objects respectively.
        """
        # ensure arrays
        if not isinstance(list_1, list):
            list_1 = []

        if not isinstance(list_2, list):
            list_2 = []

        # create hashtables for better search performance
        list_1_map = {}
        added = []
        for cur_object in list_1:
            list_1_map[str(cur_object.get_oid())] = cur_object

        # merge
        for cur_object in list_2:
            cur_oid_str = str(cur_object.get_oid())
            if not cur_oid_str in list_1_map:
                # add the object, if it doesn't exist yet
                list_1_map[cur_oid_str] = cur_object
                added.append(cur_object)

            elif isinstance(
                list_1_map[cur_oid_str], PersistentObjectProxy
            ) and isinstance(cur_object, PersistentObject):
                # overwrite a proxy by a real subject
                list_1_map[cur_oid_str] = cur_object

        return {"result": list_1_map.values(), "added": added}

    def merge_values(self, object: PersistentObject) -> Any:
        """@see PersistentObject.merge_values"""
        super().merge_values(object)
        # implement special handling for relation values
        mapper = self.get_mapper()
        for cur_relation_desc in mapper.get_relations():
            value_name = cur_relation_desc.get_other_role()
            # use parent getters to avoid loading relations
            existing_value = self.parent_get_value_method.invoke_args(
                self, [value_name]
            )
            new_value = self.parent_get_value_method.invoke_args(object, [value_name])
            if new_value != None:
                if cur_relation_desc.is_multi_valued():
                    merge_result = self.merge_object_lists(existing_value, new_value)
                    new_value = merge_result["result"]

                self.set_value_internal(value_name, new_value)

    def remove_value(self, name: Any) -> Any:
        """@see PersistentObject.remove_value()"""
        super().remove_value(name)
        # set relation state to loaded in order to prevent lazy initialization
        mapper = self.get_mapper()
        if mapper.has_relation(name):
            self.relation_states[name] = self.RELATION_STATE_LOADED

    def set_node_order(
        self, ordered_list: list, moved_list: list = None, role: Any = None
    ) -> Any:
        """Define the order of related Node instances. The mapper is responsible for
        persisting the order of the given Node instances in relation to this Node.
           @note Note instances, that are not explicitly sortable by a sortkey (@see
        PersistenceMapper.get_default_order()) will be ignored. If a given Node instance
        is not related to this Node yet, an exception will be thrown. Any not persisted
        definition of a previous call will be overwritten
           @param ordered_list Array of ordered Node instances
           @param moved_list Array of repositioned Node instances (optional, improves
        performance)
           @param role Role name of the Node instances (optional)
        """
        self.ordered_nodes = {
            "ordered": ordered_list,
            "moved": moved_list,
            "role": role,
        }
        self.set_state(PersistentObject.STATE_DIRTY)

    def set_value(
        self, name: Any, value: Any, force_set: Any = False, track_change: Any = True
    ) -> Any:
        # if the attribute is a relation, a special handling is required
        mapper = self.get_mapper()
        if mapper.has_relation(name):
            if not isinstance(value, list):
                value = [value]

            # clean the value
            super().set_value(name, None, True, False)
            # delegate to add_node
            result = True
            for i in range(len(value)):
                cur_value = value[i]
                if cur_value != None:
                    result &= self.add_node(cur_value, name, force_set, track_change)

            self.relation_states[name] = self.RELATION_STATE_INITIALIZED
            return result

        # default behaviour
        return super().set_value(name, value, force_set, track_change)
