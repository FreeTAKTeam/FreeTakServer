from digitalpy.routing.impl.default_action_mapper import DefaultActionMapper


class EmergencyActionMapper(DefaultActionMapper):
    """this is the Emergency component action mapper, each component
    must have its own action mapper to be loaded with the internal
    action mapping configuration and to be used by the facade for
    internal routing"""
