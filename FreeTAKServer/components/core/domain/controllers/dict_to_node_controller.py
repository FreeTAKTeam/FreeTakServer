from digitalpy.routing.controller import Controller


class DictToNodeController(Controller):
    def convert_dict_to_node(self, dictionary, node, **kwargs):
        self.response.set_value("model_object", self.serialize(dictionary, node))

    def serialize(self, dictionary, node):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.convert_dict_to_node(value, getattr(node, key))
            else:
                setattr(node, key, value)
        return node
