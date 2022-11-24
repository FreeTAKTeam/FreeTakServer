from digitalpy.routing.impl.default_action_mapper import DefaultActionMapper


class DomainActionMapper(DefaultActionMapper):
    """this is the Domain component action mapper, each component
    must have its own action mapper to be loaded with the internal
    action mapping configuration and to be used by the facade for
    internal routing"""
