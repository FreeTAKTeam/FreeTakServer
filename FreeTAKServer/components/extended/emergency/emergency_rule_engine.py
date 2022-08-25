from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from .domain import Event
import rule_engine

class EmergencyRuleEngine(Controller):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        context = rule_engine.Context(resolver=rule_engine.resolve_attribute)
        self.create_emergency_alert_rule = rule_engine.Rule('type == "EmergencyAlert"', context=context)
        self.create_emergency_contact_rule = rule_engine.Rule('type == "EmergencyInContact"', context=context)
        self.create_emergency_ring_the_bell_rule = rule_engine.Rule('type == "EmergencyRingTheBell"', context=context)
        self.create_emergency_geofence_breached_rule = rule_engine.Rule('type == "EmergencyGeoFenceBreached"', context=context)
        self.delete_emergency_rule = rule_engine.Rule('type == "EmergencyCancelled"', context=context)
        