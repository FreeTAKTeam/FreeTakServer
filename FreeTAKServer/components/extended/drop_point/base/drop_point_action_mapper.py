from digitalpy.routing.impl.default_action_mapper import DefaultActionMapper


class DropPointActionMapper(DefaultActionMapper):
    """This is the DropPoint component action mapper.

    Each component must have its own action mapper to be loaded with the internal
    action mapping configuration and to be used by the facade for internal routing.
    """