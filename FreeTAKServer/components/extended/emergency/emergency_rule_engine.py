from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from .domain import Event
import rule_engine

class EmergencyRuleEngine(Controller):
    def __init__(self):
        self.create_emergency_alert_rule = rule_engine.Rule('type == "b-a-o-tbl"')
        self.create_emergency_contact_rule = rule_engine.Rule('type == "b-a-o-opn"')
        self.create_emergency_ring_the_bell_rule = rule_engine.Rule('type == "b-a-o-pan"')
        self.create_emergency_geofence_breached_rule = rule_engine.Rule('type == "b-a-g"')
        
        self.delete_emergency_rule = rule_engine.Rule('type == "b-a-o-can"')