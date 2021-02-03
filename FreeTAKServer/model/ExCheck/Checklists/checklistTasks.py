from FreeTAKServer.model.ExCheck.Checklists.checklistTask import checklistTask


class checklistTasks:
    def __init__(self):
        self.checklistTask = []
        self.__count = 0

    def setchecklistTask(self, checklistTaskobj):
        if isinstance(checklistTaskobj, checklistTask):
            self.checklistTask.append(checklistTaskobj)
        else:
            raise TypeError('unsupported type')

    def getchecklistTask(self):
        obj = self.checklistTask[self.__count]
        self.__count += 1
        return obj
