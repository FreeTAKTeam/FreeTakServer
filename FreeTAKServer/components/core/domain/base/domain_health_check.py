from digitalpy.component.impl.default_health_check import DefaultHealthCheckController


class DomainHealthCheck(DefaultHealthCheckController):
    """this class only inherits from the default health check controller so that the internal \
    action mapper maps to a local controller"""
