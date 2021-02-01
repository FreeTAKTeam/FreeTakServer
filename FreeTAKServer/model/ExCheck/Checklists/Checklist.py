from FreeTAKServer.model.ExCheck.Checklists.checklistDetails import checklistDetails
from FreeTAKServer.model.ExCheck.Checklists.checklistColumns import checklistColumns
from FreeTAKServer.model.ExCheck.Checklists.checklistTasks import checklistTasks

class Checklist:
    def __init__(self):
        self.checklistDetails = checklistDetails()
        self.checklistColumns = checklistColumns()
        self.checklistTasks = checklistTasks()
