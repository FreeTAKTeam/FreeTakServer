from FreeTAKServer.model.ExCheck.Checklists.Checklist import Checklist
from defusedxml import ElementTree as etree

class generateChecklist:
    def __init__(self, template):
        self.checklist = Checklist()
        self.template = template
    def generate_tasks(self):
        xml = etree.fromstring(self.template)
        xml.Element('')